import json
import urllib.request
import urllib.error

class LeetCodeClient:
    def __init__(self, username):
        self.username = username
        self.url = "https://leetcode.com/graphql"
        
    def fetch_stats(self):
        query = """
        query getUserStats($username: String!) {
          matchedUser(username: $username) {
            submitStats {
              acSubmissionNum {
                difficulty
                count
              }
            }
          }
        }
        """
        
        fallback_data = {
            "easy": 45,
            "medium": 72,
            "hard": 18,
            "total": 135
        }
        
        if not self.username:
            return fallback_data
            
        data = json.dumps({"query": query, "variables": {"username": self.username}}).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                
                if "errors" in res_data or not res_data.get("data") or not res_data["data"].get("matchedUser"):
                    print("LeetCode GraphQL error or user not found. Falling back.")
                    return fallback_data
                    
                stats_list = res_data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
                
                stats = {}
                for stat in stats_list:
                    diff = stat["difficulty"].lower()
                    stats[diff] = stat["count"]
                    
                return {
                    "easy": stats.get("easy", 0),
                    "medium": stats.get("medium", 0),
                    "hard": stats.get("hard", 0),
                    "total": stats.get("all", 0)
                }
        except urllib.error.URLError as e:
            print("Network error fetching LeetCode stats:", e)
            return fallback_data
        except Exception as e:
            print("Unexpected error during LeetCode fetch:", e)
            return fallback_data
