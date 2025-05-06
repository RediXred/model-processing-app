from typing import Dict


class ConfigComparator:
    def compare_configs(self, original: Dict, patched: Dict) -> Dict:
        delta = {"additions": [], "deletions": [], "updates": []}
        
        for key in patched:
            if key not in original:
                delta["additions"].append({"key": key, "value": patched[key]})
        
        for key in original:
            if key not in patched:
                delta["deletions"].append(key)
        
        for key in original:
            if key in patched and original[key] != patched[key]:
                delta["updates"].append({"key": key, "from": original[key], "to": patched[key]})
        
        return delta
    
    def apply_delta(self, original: Dict, delta: Dict) -> Dict:
        result = original.copy()
        
        for key in delta["deletions"]:
            result.pop(key, None)
        
        for update in delta["updates"]:
            result[update["key"]] = update["to"]
        
        for addition in delta["additions"]:
            result[addition["key"]] = addition["value"]
        
        return result