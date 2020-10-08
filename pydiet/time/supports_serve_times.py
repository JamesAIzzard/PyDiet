
class SupportsServeTimes:
    @property
    def serve_times_summary(self) -> str:
        return 'Serve times summary'

class SupportsSettingServeTimes(SupportsServeTimes):
    ...
