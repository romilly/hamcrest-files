import os

from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description

def read(f):
    with open(f) as input_file:
        return input_file.read()


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
        return os.path.isdir(item) and self.contents_match(item)

    def contents_match(self, item):
        contents = self.get_contents(item)
        return set(contents) == set(self.paths)

    def get_contents(self, item):
        contents = []
        for root, directories, files in os.walk(item):
            for file in files:
                relpath = os.path.relpath(root, item)
                if relpath == '.':
                    contents.append(file)
                else:
                    contents.append(os.path.join(relpath, file))
        return contents

    def describe_to(self, description: Description) -> None:
        description.append_text('a directory containing %s' % ', '.join(self.paths))

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        super().describe_mismatch(item, mismatch_description)
        if not os.path.isdir(item):
            mismatch_description.append_text(' which is not a directory')
        elif 0 ==len(os.listdir(item)):
            mismatch_description.append_text(' which is an empty directory')
        else:
            mismatch_description.append_text(' which contains %s' % ', '.join(self.get_contents(item)))


def contains_files(*paths):
    return DirectoryContentsMatcher(paths)


class FileContentMatcher(BaseMatcher):
    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        if not os.path.isfile(item):
            mismatch_description.append_text('%s was not a file' % item)
        else:
            mismatch_description.append_text('a file with contents %s' % read(item))

    def _matches(self, item: T) -> bool:
        if not os.path.isfile(item):
            return False
        return self.content_matcher.matches(read(item))

    def describe_to(self, description: Description) -> None:
        description.append_text('a file with contents ')
        self.content_matcher.describe_to(description)

    def __init__(self, matcher: BaseMatcher):
        self.content_matcher = matcher


def file_content(matcher):
    return FileContentMatcher(matcher)