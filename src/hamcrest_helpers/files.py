import os

from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description


class EmptyDirectoryMatcher(BaseMatcher):
    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        super().describe_mismatch(item, mismatch_description)
        if not os.path.isdir(item):
            mismatch_description.append_text(' which is not a directory')
        else:
            mismatch_description.append_text(' which contains %s' % ', '.join(os.listdir(item)))

    def describe_to(self, description: Description) -> None:
        description.append_text('an empty directory')

    def _matches(self, item: T) -> bool:
        return os.path.isdir(item) and 0 == len(os.listdir(item))


def is_empty_directory():
    return EmptyDirectoryMatcher()


class DirectoryContentsMatcher(BaseMatcher):
    def __init__(self, paths):
        self.paths = paths

    def _matches(self, item: T) -> bool:
        return os.path.isdir(item) and set(os.listdir(item)) == set(self.paths)

    def describe_to(self, description: Description) -> None:
        description.append_text('a directory containing %s' % ', '.join(self.paths))

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        super().describe_mismatch(item, mismatch_description)
        if not os.path.isdir(item):
            mismatch_description.append_text(' which is not a directory')
        elif 0 ==len(os.listdir(item)):
            mismatch_description.append_text(' which is an empty directory')
        else:
            mismatch_description.append_text(' which contains %s' % ', '.join(os.listdir(item)))

def contains_files(*paths):
    return DirectoryContentsMatcher(paths)