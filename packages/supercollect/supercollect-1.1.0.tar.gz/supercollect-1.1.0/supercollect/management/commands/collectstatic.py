from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
    staticfiles_storage,
)

from supercollect.utils import get_all_files
import json


class Command(collectstatic.Command):
    """
    Uses FileSystemStorage to collect and post-process files.
    Then, files are uploaded.
    This significantly speeds up the process for remote locations.
    """
    turbo_report = {"modified": 0, "unmodified": 0}

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--turbo",
            action="store_true",
            help="Use turbo mode.",
        )
        parser.add_argument(
            "--nodiff",
            action="store_true",
            help="Skip manifest diffing.",
        )

    def set_options(self, **options):
        super().set_options(**options)
        self.turbo = options["turbo"]
        self.manifest_diffing_enabled = not options["nodiff"]

    
    def get_files(self, storage):
        for filepath in get_all_files(storage):
            # Skip source files to minimize uploaded objects w/ manifest deployments
            if self.manifest_contents and filepath in self.manifest_contents:
                continue
            yield filepath


    def collect(self):
        manifest_deployment, temp_storage = False, None

        if self.turbo:
            if hasattr(staticfiles_storage, "manifest_version"):
                manifest_deployment = True

            self.storage = temp_storage = (
                ManifestStaticFilesStorage(location=settings.STATIC_ROOT)
                if manifest_deployment
                else StaticFilesStorage(location=settings.STATIC_ROOT)
            )

        is_dry_run = self.dry_run

        if is_dry_run and self.turbo:
            self.dry_run = False
        
        report = super().collect()

        if not self.turbo:
            return report

        if manifest_deployment:
            try:
                with temp_storage.open("staticfiles.json") as manifest:
                    manifest_file = manifest.read().decode()
                    self.manifest_contents = json.loads(manifest_file)["paths"]
            except FileNotFoundError:
                self.manifest_contents = None
        else:
            self.manifest_contents = None

        if is_dry_run:
            self.dry_run = True

        self.storage = staticfiles_storage
        get_files_to_upload = lambda: self.get_files(temp_storage)

        if manifest_deployment and self.manifest_diffing_enabled:
            # Read old manifest
            try:
                with self.storage.open("staticfiles.json") as manifest:
                    old_manifest = manifest.read().decode()
            except FileNotFoundError:
                old_manifest = None

            if old_manifest and self.manifest_contents:
                # Do diffing to determine which files to update
                old_manifest_contents = json.loads(old_manifest)["paths"]

                def get_changed_files():
                    for file_path in self.manifest_contents:
                        if file_path not in old_manifest_contents or old_manifest_contents[file_path] != self.manifest_contents[file_path]:
                            yield self.manifest_contents[file_path]
                        else:
                            self.turbo_report["unmodified"] += 1
                    
                    yield "staticfiles.json"

                get_files_to_upload = lambda: get_changed_files()

        with ThreadPoolExecutor() as executor:
            for file in get_files_to_upload():
                if not self.dry_run:
                    executor.submit(self.upload, file, temp_storage)
                self.turbo_report["modified"] += 1

        return report

    def handle(self, **options):
        report = super().handle(**options)

        if not self.turbo:
            # Vanilla Django Report
            return report
        
        report = self.turbo_report

        if self.dry_run:
            return f"super().would_have_collected(modified={str(report['modified'])}, unmodified={str(report['unmodified'])})"
        
        return f"super().collected(modified={str(report['modified'])}, unmodified={str(report['unmodified'])})"

    def upload(self, path, source_storage):
        with source_storage.open(path) as source_file:
            self.storage.save(path, source_file)
