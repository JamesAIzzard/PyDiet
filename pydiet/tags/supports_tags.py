
class SupportsTags:
    @property
    def tag_summary(self) -> str:
        return 'Tag summary.'

class SupportsSettingTags(SupportsTags):
    ...