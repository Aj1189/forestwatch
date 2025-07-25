# report_analyzer/analyzer.py

class ReportAnalyzer:
    def __init__(self):
        self.complaints = []

    def load_complaints(self, complaints):
        """Takes a list of Complaint model instances"""
        self.complaints = complaints

    def count_by_category(self):
        keys = []
        counts = []
        for c in self.complaints:
            cat = c.category.lower()
            if cat in keys:
                idx = keys.index(cat)
                counts[idx] += 1
            else:
                keys.append(cat)
                counts.append(1)
        return list(zip(keys, counts))

    def count_by_region(self):
        keys = []
        counts = []
        for c in self.complaints:
            region = (c.user.region or "unknown").lower()
            if region in keys:
                idx = keys.index(region)
                counts[idx] += 1
            else:
                keys.append(region)
                counts.append(1)
        return list(zip(keys, counts))

    def count_by_month(self):
        keys = []
        counts = []
        for c in self.complaints:
            dt = c.created_at
            month_key = f"{dt.year}-{str(dt.month).zfill(2)}"
            if month_key in keys:
                idx = keys.index(month_key)
                counts[idx] += 1
            else:
                keys.append(month_key)
                counts.append(1)
        return list(zip(keys, counts))

    def frequent_regions(self, threshold=2):
        regions = []
        counts = []
        for c in self.complaints:
            region = (c.user.region or "unknown").lower()
            if region in regions:
                idx = regions.index(region)
                counts[idx] += 1
            else:
                regions.append(region)
                counts.append(1)
        result = []
        for i in range(len(regions)):
            if counts[i] >= threshold:
                result.append((regions[i], counts[i]))
        return result
