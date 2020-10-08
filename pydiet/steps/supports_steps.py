
class SupportsSteps:
    @property
    def step_summary(self) -> str:
        return 'Step summary.'

class SupportsSettingSteps(SupportsSteps):
    ...