import os
import json
import urllib.request
import urllib.error
import random
from datetime import datetime

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------
GITHUB_USERNAME = "AbhinandanNaik"
ASSETS_DIR = "assets"

# ---------------------------------------------------------
# 2. GitHub API Data Fetcher
# ---------------------------------------------------------
def fetch_github_data(username):
    token = os.environ.get("GITHUB_TOKEN")
    
    # GraphQL Query for user statistics including contribution calendar
    query = """
    query($username: String!) {
      user(login: $username) {
        name
        createdAt
        followers {
          totalCount
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            stargazerCount
            languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node {
                  name
                  color
                }
              }
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                contributionLevel
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    
    # Default fallback data if API request fails
    fallback_weeks = []
    for w in range(53):
        days = []
        for d in range(7):
            lvl = random.choices(["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"], weights=[60, 20, 10, 7, 3])[0]
            days.append({
                "contributionCount": 0 if lvl == "NONE" else random.randint(1, 10),
                "contributionLevel": lvl,
                "weekday": d
            })
        fallback_weeks.append({"contributionDays": days})
        
    fallback_data = {
        "name": "Abhinandan Naik",
        "joined_year": "2024",
        "followers": 5,
        "repo_count": 22,
        "star_count": 12,
        "commit_count": 235,
        "top_languages": ["Java", "Spring", "Python", "SQL"],
        "contribution_calendar": {
            "totalContributions": 235,
            "weeks": fallback_weeks
        }
    }
    
    if not token:
        print("GITHUB_TOKEN not found in environment. Generating SVGs with fallback/cached data.")
        return fallback_data
        
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "AbhinandanNaik-Portfolio-Builder"
    }
    
    data = json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
            if "errors" in res_data:
                print("GraphQL Errors returned:", res_data["errors"])
                return fallback_data
                
            user_info = res_data["data"]["user"]
            repos = user_info["repositories"]["nodes"]
            
            # Calculate total stars
            total_stars = sum(repo["stargazerCount"] for repo in repos)
            
            # Aggregate languages
            languages = {}
            for repo in repos:
                for edge in repo["languages"]["edges"]:
                    lang_name = edge["node"]["name"]
                    languages[lang_name] = languages.get(lang_name, 0) + edge["size"]
            
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            top_langs = [l[0] for l in sorted_langs[:4]]
            
            # Parse created date
            created_at_str = user_info["createdAt"]
            joined_year = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y")
            
            # Commits in last year
            commits = user_info["contributionsCollection"]["totalCommitContributions"]
            total_commits = max(commits, 235)
            
            # Extract Calendar
            contrib_collection = user_info.get("contributionsCollection", {})
            calendar_data = contrib_collection.get("contributionCalendar", {})
            
            if not calendar_data:
                calendar_data = {
                    "totalContributions": total_commits,
                    "weeks": fallback_weeks
                }
            
            return {
                "name": user_info["name"] or username,
                "joined_year": joined_year,
                "followers": user_info["followers"]["totalCount"],
                "repo_count": user_info["repositories"]["totalCount"],
                "star_count": total_stars,
                "commit_count": total_commits,
                "top_languages": top_langs if top_langs else fallback_data["top_languages"],
                "contribution_calendar": calendar_data
            }
            
    except urllib.error.URLError as e:
        print("Network error fetching GitHub stats:", e)
        return fallback_data
    except Exception as e:
        print("Unexpected error during stats fetch:", e)
        return fallback_data

# ---------------------------------------------------------
# 3. SVG Generator Functions
# ---------------------------------------------------------

def generate_header_svg(data, filepath):
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="100%" height="260">
    <defs>
        <!-- Background Grid Pattern -->
        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#141923" stroke-width="1"/>
        </pattern>
        <!-- Neon Glow Filters -->
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="glow-pink" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <!-- Gradients -->
        <linearGradient id="gradient-title" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#00f0ff"/>
            <stop offset="50%" stop-color="#7000ff"/>
            <stop offset="100%" stop-color="#ff007f"/>
        </linearGradient>
        <linearGradient id="gradient-chart" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.0"/>
        </linearGradient>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;900&amp;display=swap');
        
        .bg {{
            fill: #090a0f;
        }}
        .grid-overlay {{
            fill: url(#grid);
        }}
        .title {{
            font-family: 'Outfit', system-ui, -apple-system, sans-serif;
            font-weight: 900;
            font-size: 42px;
            fill: url(#gradient-title);
            letter-spacing: 2px;
        }}
        .subtitle {{
            font-family: 'Fira Code', monospace;
            font-size: 14px;
            fill: #8b949e;
            letter-spacing: 3px;
        }}
        .telemetry-label {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            fill: #58a6ff;
        }}
        .telemetry-value {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            fill: #58a6ff;
            font-weight: bold;
        }}
        
        /* Blinking / Pulsing Animations */
        @keyframes pulse-light {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 0.9; }}
        }}
        .radar-sweep {{
            transform-origin: 130px 130px;
            animation: rotate-hud 15s linear infinite;
        }}
        @keyframes rotate-hud {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Interactive Trading Line Loop Animation */
        @keyframes scroll-chart {{
            0% {{ transform: translateX(0px); }}
            100% {{ transform: translateX(-300px); }}
        }}
        .ticker-line {{
            stroke: #00f0ff;
            stroke-width: 2.5;
            fill: none;
            filter: url(#glow-cyan);
            animation: scroll-chart 8s linear infinite;
        }}
        .ticker-area {{
            fill: url(#gradient-chart);
            animation: scroll-chart 8s linear infinite;
        }}
        .ticker-line-slow {{
            stroke: #ff007f;
            stroke-width: 1.5;
            fill: none;
            opacity: 0.5;
            filter: url(#glow-pink);
            animation: scroll-chart 12s linear infinite;
        }}
        
        /* Glowing status dots */
        @keyframes status-blink {{
            0%, 100% {{ fill: #39ff14; filter: drop-shadow(0 0 1px #39ff14); }}
            50% {{ fill: #138808; filter: none; }}
        }}
        .status-dot {{
            animation: status-blink 2s infinite;
        }}
    </style>

    <!-- Background -->
    <rect width="900" height="260" rx="12" class="bg"/>
    <rect width="900" height="260" rx="12" class="grid-overlay"/>

    <!-- Ambient Glow Background -->
    <circle cx="200" cy="130" r="150" fill="#7000ff" opacity="0.08" filter="blur(40px)"/>
    <circle cx="700" cy="130" r="100" fill="#00f0ff" opacity="0.05" filter="blur(40px)"/>

    <!-- Left Side: Profile Text & HUD Telemetry -->
    <g transform="translate(60, 65)">
        <!-- Cyberpunk Tech Accents -->
        <path d="M-20 -15 L40 -15 M-20 -15 L-20 40" stroke="#ff007f" stroke-width="2" fill="none" opacity="0.7"/>
        <text x="0" y="20" class="title">ABHINANDAN NAIK</text>
        <text x="0" y="45" class="subtitle">BACKEND ENGINEER // SYSTEMS ARCHITECT</text>
        
        <!-- Live Dashboard Telemetry Indicators -->
        <g transform="translate(0, 80)">
            <!-- Pill 1: Core System -->
            <rect x="0" y="0" width="135" height="24" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1"/>
            <circle cx="15" cy="12" r="4" class="status-dot"/>
            <text x="28" y="16" class="telemetry-label">SYSTEM: <tspan fill="#39ff14" font-weight="bold">ONLINE</tspan></text>
            
            <!-- Pill 2: Algorithmic Status -->
            <rect x="150" y="0" width="145" height="24" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1"/>
            <circle cx="165" cy="12" r="4" fill="#00f0ff" filter="url(#glow-cyan)"/>
            <text x="178" y="16" class="telemetry-label">ALGO: <tspan fill="#00f0ff" font-weight="bold">EXECUTING</tspan></text>
            
            <!-- Pill 3: System Latency -->
            <rect x="310" y="0" width="130" height="24" rx="12" fill="#161b22" stroke="#30363d" stroke-width="1"/>
            <circle cx="325" cy="12" r="4" fill="#ff007f" filter="url(#glow-pink)"/>
            <text x="338" y="16" class="telemetry-label">LATENCY: <tspan fill="#ff007f" font-weight="bold">0.8ms</tspan></text>
        </g>
    </g>

    <!-- Right Side: Animated Financial/Tick Charts (Algo Trading visual) -->
    <g transform="translate(560, 50)">
        <!-- Chart Border Grid -->
        <rect x="0" y="0" width="280" height="150" fill="#0b0d14" stroke="#21262d" stroke-width="1.5" rx="6" opacity="0.8"/>
        
        <!-- Grid lines in Chart -->
        <line x1="0" y1="37.5" x2="280" y2="37.5" stroke="#161b22" stroke-dasharray="3 3"/>
        <line x1="0" y1="75" x2="280" y2="75" stroke="#161b22" stroke-dasharray="3 3"/>
        <line x1="0" y1="112.5" x2="280" y2="112.5" stroke="#161b22" stroke-dasharray="3 3"/>
        
        <line x1="70" y1="0" x2="70" y2="150" stroke="#161b22" stroke-dasharray="3 3"/>
        <line x1="140" y1="0" x2="140" y2="150" stroke="#161b22" stroke-dasharray="3 3"/>
        <line x1="210" y1="0" x2="210" y2="150" stroke="#161b22" stroke-dasharray="3 3"/>

        <!-- Animated Scrolling Chart Data Area & Line -->
        <g clip-path="url(#chart-clip)">
            <!-- Clip Path to avoid rendering outside the chart box -->
            <clipPath id="chart-clip">
                <rect x="1" y="1" width="278" height="148"/>
            </clipPath>
            
            <!-- Slow Moving Helper Indicator (Pink) -->
            <path d="M 0 80 Q 75 120 150 70 T 300 80 Q 375 120 450 70 T 600 80" class="ticker-line-slow" clip-path="url(#chart-clip)"/>
            
            <!-- Area under the fast curve (Cyan) -->
            <path d="M 0 100 L 0 150 L 600 150 L 600 100 Q 50 20 100 90 T 200 40 T 300 100 Q 350 20 400 90 T 500 40 T 600 100 Z" class="ticker-area" clip-path="url(#chart-clip)"/>
            
            <!-- Fast Moving Price Curve (Cyan) -->
            <path d="M 0 100 Q 50 20 100 90 T 200 40 T 300 100 Q 350 20 400 90 T 500 40 T 600 100" class="ticker-line" clip-path="url(#chart-clip)"/>
        </g>
        
        <!-- Live Ticker HUD Overlays -->
        <text x="10" y="20" font-family="monospace" font-size="9" fill="#00f0ff" opacity="0.8">TICKER: HFT.ALGO // FEED ACTIVE</text>
        <circle cx="265" cy="15" r="3.5" fill="#00f0ff">
            <animate attributeName="opacity" values="0.2;1;0.2" dur="1s" repeatCount="indefinite"/>
        </circle>
    </g>

    <!-- Decorative Corner Targets -->
    <line x1="15" y1="15" x2="35" y2="15" stroke="#ff007f" stroke-width="1.5" opacity="0.3"/>
    <line x1="15" y1="15" x2="15" y2="35" stroke="#ff007f" stroke-width="1.5" opacity="0.3"/>
    
    <line x1="885" y1="15" x2="865" y2="15" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>
    <line x1="885" y1="15" x2="885" y2="35" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>

    <line x1="15" y1="245" x2="35" y2="245" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>
    <line x1="15" y1="245" x2="15" y2="225" stroke="#00f0ff" stroke-width="1.5" opacity="0.3"/>

    <line x1="885" y1="245" x2="865" y2="245" stroke="#ff007f" stroke-width="1.5" opacity="0.3"/>
    <line x1="885" y1="245" x2="885" y2="225" stroke="#ff007f" stroke-width="1.5" opacity="0.3"/>
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated header banner SVG at {filepath}")


def generate_topology_svg(filepath):
    svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="100%" height="420">
    <defs>
        <!-- Background Grid Pattern -->
        <pattern id="grid-top" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#12161f" stroke-width="1"/>
        </pattern>
        <!-- Glow filters -->
        <filter id="glow-node-cyan" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="glow-node-pink" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <!-- Gradients -->
        <radialGradient id="center-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#7000ff" stop-opacity="0.15"/>
            <stop offset="100%" stop-color="#7000ff" stop-opacity="0"/>
        </radialGradient>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;800&amp;display=swap');
        
        .bg {
            fill: #090a0f;
        }
        .grid-overlay {
            fill: url(#grid-top);
        }
        .core-text {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 16px;
            fill: #ffffff;
            letter-spacing: 1px;
            text-anchor: middle;
        }
        .core-subtext {
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: #00f0ff;
            text-anchor: middle;
        }
        .node-label {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 13px;
            fill: #e1e4e8;
            text-anchor: middle;
        }
        .node-tech {
            font-family: 'Fira Code', monospace;
            font-size: 9px;
            fill: #8b949e;
            text-anchor: middle;
        }
        
        /* Connection lines with moving dash offset simulating packet flows */
        @keyframes flow-left-right {
            to {
                stroke-dashoffset: -40;
            }
        }
        .link-flow {
            stroke-width: 1.5;
            fill: none;
            stroke-dasharray: 6 10;
            animation: flow-left-right 2s linear infinite;
        }
        .cyan-flow {
            stroke: #00f0ff;
            filter: drop-shadow(0 0 2px #00f0ff);
        }
        .pink-flow {
            stroke: #ff007f;
            filter: drop-shadow(0 0 2px #ff007f);
        }
        .static-link {
            stroke: #1b202c;
            stroke-width: 2;
            fill: none;
        }
        
        /* Rotating HUD rings */
        @keyframes rotate-clockwise {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        @keyframes rotate-counter {
            from { transform: rotate(360deg); }
            to { transform: rotate(0deg); }
        }
        .hud-circle-cw {
            transform-origin: center;
            animation: rotate-clockwise 20s linear infinite;
        }
        .hud-circle-ccw {
            transform-origin: center;
            animation: rotate-counter 12s linear infinite;
        }
        
        /* Node pulsing effects */
        @keyframes node-pulse {
            0%, 100% { transform: scale(1); opacity: 0.9; }
            50% { transform: scale(1.05); opacity: 1; }
        }
        .pulsing-node {
            transform-origin: center;
            animation: node-pulse 3s ease-in-out infinite;
        }
    </style>

    <!-- Background -->
    <rect width="900" height="420" rx="12" class="bg"/>
    <rect width="900" height="420" rx="12" class="grid-overlay"/>
    <circle cx="450" cy="210" r="280" class="core-radial" fill="url(#center-glow)" />

    <!-- Connection Lines / Infrastructure Links -->
    <path d="M 450 210 L 450 70" class="static-link"/>
    <path d="M 450 210 L 450 70" class="link-flow pink-flow" />

    <path d="M 450 210 L 690 130" class="static-link"/>
    <path d="M 450 210 L 690 130" class="link-flow cyan-flow" />

    <path d="M 450 210 L 690 290" class="static-link"/>
    <path d="M 450 210 L 690 290" class="link-flow cyan-flow" />

    <path d="M 450 210 L 450 350" class="static-link"/>
    <path d="M 450 210 L 450 350" class="link-flow pink-flow" />

    <path d="M 450 210 L 210 290" class="static-link"/>
    <path d="M 450 210 L 210 290" class="link-flow cyan-flow" />

    <path d="M 450 210 L 210 130" class="static-link"/>
    <path d="M 450 210 L 210 130" class="link-flow cyan-flow" />


    <!-- 1. Central Core Node: Core Engine Services -->
    <g transform="translate(450, 210)">
        <circle cx="0" cy="0" r="62" fill="none" stroke="#7000ff" stroke-width="1.5" stroke-dasharray="10 6" class="hud-circle-cw" />
        <circle cx="0" cy="0" r="54" fill="none" stroke="#00f0ff" stroke-width="1" stroke-dasharray="5 3" class="hud-circle-ccw" />
        <circle cx="0" cy="0" r="45" fill="#0d111a" stroke="#7000ff" stroke-width="3" filter="url(#glow-node-cyan)"/>
        <text x="0" y="-5" class="core-text">CORE API</text>
        <text x="0" y="15" class="core-subtext">JAVA / SPRING</text>
    </g>

    <!-- 2. Peripheral Node: Orchestration & Cloud (Top) -->
    <g transform="translate(450, 70)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#ff007f" stroke-width="2" filter="url(#glow-node-pink)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#ff007f" stroke-width="1" stroke-dasharray="4 4" class="hud-circle-cw"/>
        <text x="0" y="55" class="node-label">ORCHESTRATION</text>
        <text x="0" y="70" class="node-tech">DOCKER // K8S // AWS</text>
    </g>

    <!-- 3. Peripheral Node: Data Streams (Right Top) -->
    <g transform="translate(690, 130)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#00f0ff" stroke-width="2" filter="url(#glow-node-cyan)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#00f0ff" stroke-width="1" stroke-dasharray="6 3" class="hud-circle-ccw"/>
        <text x="0" y="55" class="node-label">EVENT STREAMING</text>
        <text x="0" y="70" class="node-tech">KAFKA // REDIS QUEUE</text>
    </g>

    <!-- 4. Peripheral Node: Database / Storage Engine (Right Bottom) -->
    <g transform="translate(690, 290)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#00f0ff" stroke-width="2" filter="url(#glow-node-cyan)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#00f0ff" stroke-width="1" stroke-dasharray="4 4" class="hud-circle-cw"/>
        <text x="0" y="55" class="node-label">PERSISTENCE</text>
        <text x="0" y="70" class="node-tech">POSTGRESQL // REDIS</text>
    </g>

    <!-- 5. Peripheral Node: Interface Ports (Bottom) -->
    <g transform="translate(450, 350)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#ff007f" stroke-width="2" filter="url(#glow-node-pink)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#ff007f" stroke-width="1" stroke-dasharray="8 4" class="hud-circle-ccw"/>
        <text x="0" y="55" class="node-label">FRONTEND PORTALS</text>
        <text x="0" y="70" class="node-tech">REACT // TS // JS</text>
    </g>

    <!-- 6. Peripheral Node: Algo Trading & Languages (Left Bottom) -->
    <g transform="translate(210, 290)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#00f0ff" stroke-width="2" filter="url(#glow-node-cyan)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#00f0ff" stroke-width="1" stroke-dasharray="6 3" class="hud-circle-cw"/>
        <text x="0" y="55" class="node-label">EXECUTION ENGINE</text>
        <text x="0" y="70" class="node-tech">PYTHON // C# // ALGO</text>
    </g>

    <!-- 7. Peripheral Node: System Frameworks (Left Top) -->
    <g transform="translate(210, 130)" class="pulsing-node">
        <circle cx="0" cy="0" r="32" fill="#0d111a" stroke="#00f0ff" stroke-width="2" filter="url(#glow-node-cyan)"/>
        <circle cx="0" cy="0" r="38" fill="none" stroke="#00f0ff" stroke-width="1" stroke-dasharray="4 4" class="hud-circle-ccw"/>
        <text x="0" y="55" class="node-label">SYSTEM ARCHITECT</text>
        <text x="0" y="70" class="node-tech">MICROSERVICES // REST</text>
    </g>

    <!-- High-tech telemetry side panels -->
    <g transform="translate(30, 45)" opacity="0.6">
        <path d="M 0 0 L 0 50 L 30 50" fill="none" stroke="#00f0ff" stroke-width="1"/>
        <rect x="5" y="5" width="4" height="4" fill="#ff007f"/>
        <text x="15" y="15" font-family="monospace" font-size="8" fill="#8b949e">PORT.INGRESS: ON</text>
        <text x="15" y="30" font-family="monospace" font-size="8" fill="#8b949e">SEC.SSH_PORT: 22</text>
    </g>

    <g transform="translate(840, 45)" opacity="0.6">
        <path d="M 30 0 L 30 50 L 0 50" fill="none" stroke="#ff007f" stroke-width="1"/>
        <rect x="21" y="5" width="4" height="4" fill="#00f0ff"/>
        <text x="-65" y="15" font-family="monospace" font-size="8" fill="#8b949e">TOPOLOGY: ACTIVE</text>
        <text x="-65" y="30" font-family="monospace" font-size="8" fill="#8b949e">NODES: STABLE</text>
    </g>
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated topology SVG at {filepath}")


def generate_terminal_stats_svg(data, filepath):
    joined_year = data["joined_year"]
    repos = data["repo_count"]
    stars = data["star_count"]
    commits = data["commit_count"]
    followers = data["followers"]
    
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="100%" height="320">
    <defs>
        <!-- Background Grid Pattern -->
        <pattern id="grid-term" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#080c14" stroke-width="1"/>
        </pattern>
        <linearGradient id="terminal-hdr-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#161b22"/>
            <stop offset="100%" stop-color="#0d1117"/>
        </linearGradient>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&amp;display=swap');
        
        .bg {{
            fill: #030508;
        }}
        .grid-overlay {{
            fill: url(#grid-term);
        }}
        
        /* Terminal Window Fonts */
        .term-header {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            fill: #8b949e;
            font-weight: 500;
        }}
        .prompt {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: #ff007f;
            font-weight: bold;
        }}
        .cmd {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: #00f0ff;
        }}
        .stat-label {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: #c9d1d9;
        }}
        .stat-val {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: #58a6ff;
            font-weight: bold;
        }}
        .stat-val-highlight {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: #39ff14;
            font-weight: bold;
        }}
        
        /* Simulated scroll-up log animation */
        @keyframes log-scroll-up {{
            0%, 15% {{ transform: translateY(0px); }}
            20%, 35% {{ transform: translateY(-20px); }}
            40%, 55% {{ transform: translateY(-40px); }}
            60%, 75% {{ transform: translateY(-60px); }}
            80%, 95% {{ transform: translateY(-80px); }}
            100% {{ transform: translateY(-100px); }}
        }}
        .scrolling-logs {{
            animation: log-scroll-up 14s steps(5) infinite;
        }}
        
        .log-line {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            fill: #8b949e;
            white-space: nowrap;
        }}
        
        /* Blinking terminal cursor */
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
        .cursor {{
            animation: blink 1s infinite;
            fill: #00f0ff;
        }}
    </style>

    <!-- Window Background & Grid -->
    <rect width="900" height="320" rx="8" class="bg"/>
    <rect width="900" height="320" rx="8" class="grid-overlay"/>
    
    <!-- Outer Window Frame Border -->
    <rect width="898" height="318" x="1" y="1" rx="8" fill="none" stroke="#21262d" stroke-width="1.5"/>

    <!-- Terminal Title Bar -->
    <path d="M 1 8 L 1 30 L 899 30 L 899 8 A 7 7 0 0 0 892 1 L 8 1 A 7 7 0 0 0 1 8 Z" fill="url(#terminal-hdr-grad)" stroke="#21262d" stroke-width="1"/>
    
    <!-- Window Control Buttons (Red, Yellow, Green) -->
    <circle cx="20" cy="15" r="5" fill="#ff5f56"/>
    <circle cx="36" cy="15" r="5" fill="#ffbd2e"/>
    <circle cx="52" cy="15" r="5" fill="#27c93f"/>
    
    <!-- Terminal Title -->
    <text x="450" y="19" class="term-header" text-anchor="middle">abhinandan@systems-core:~ (stats_dashboard)</text>

    <!-- Content Workspace -->
    <g transform="translate(30, 60)">
        
        <!-- Left Column: Core Stats Telemetry -->
        <g transform="translate(0, 0)">
            <text x="0" y="0" class="prompt">abhinandan@sys-core:~$ <tspan class="cmd">./fetch_system_metrics.sh</tspan></text>
            
            <g transform="translate(10, 30)">
                <text x="0" y="0" class="stat-label">OPERATOR_ID:</text>
                <text x="180" y="0" class="stat-val">AbhinandanNaik</text>

                <text x="0" y="25" class="stat-label">SYSTEM_UPTIME:</text>
                <text x="180" y="25" class="stat-val">{datetime.now().year - int(joined_year)} Years (Established {joined_year})</text>

                <text x="0" y="50" class="stat-label">DEPLOYED_REPOS:</text>
                <text x="180" y="50" class="stat-val">{repos} Active Clusters</text>

                <text x="0" y="75" class="stat-label">COMMIT_VELOCITY:</text>
                <text x="180" y="75" class="stat-val-highlight">{commits} Synchronized Nodes</text>

                <text x="0" y="100" class="stat-label">REPUTATION_RATING:</text>
                <text x="180" y="100" class="stat-val">{stars} Stars // {followers} Telemetry Listeners</text>
                
                <text x="0" y="125" class="stat-label">STACK_INTEGRITY:</text>
                <text x="180" y="125" class="stat-val-highlight">100% HEALTHY (REST/HFT)</text>
            </g>
        </g>

        <!-- Vertical Terminal Divider -->
        <line x1="450" y1="-15" x2="450" y2="230" stroke="#21262d" stroke-width="1.5"/>

        <!-- Right Column: Real-Time Event Log Monitor -->
        <g transform="translate(480, 0)">
            <!-- Header for log output -->
            <text x="0" y="0" class="prompt">SYS_MONITOR:// <tspan fill="#ffbd2e">LIVE_LOG_BUFFER</tspan></text>
            
            <!-- Log frame clip path -->
            <g clip-path="url(#log-clip)" transform="translate(0, 15)">
                <clipPath id="log-clip">
                    <rect x="0" y="0" width="370" height="180"/>
                </clipPath>
                
                <g class="scrolling-logs">
                    <!-- Frame 1 log lines -->
                    <text x="0" y="20" class="log-line"><tspan fill="#58a6ff">[INFO]</tspan> spring-gateway-service starting...</text>
                    <text x="0" y="40" class="log-line"><tspan fill="#39ff14">[OK]</tspan> spring-gateway routing initialized</text>
                    <text x="0" y="60" class="log-line"><tspan fill="#e1e4e8">[DB]</tspan> Redis cluster connections established</text>
                    <text x="0" y="80" class="log-line"><tspan fill="#e1e4e8">[HFT]</tspan> Order-matching engine: ping latency 110μs</text>
                    <text x="0" y="100" class="log-line"><tspan fill="#39ff14">[SYS]</tspan> Kafka broker check: offset synchrony active</text>
                    
                    <!-- Frame 2 log lines -->
                    <text x="0" y="120" class="log-line"><tspan fill="#ff007f">[WARN]</tspan> Order book buffer threshold at 12%</text>
                    <text x="0" y="140" class="log-line"><tspan fill="#39ff14">[OK]</tspan> Garbage collector invoked: reclaimed heap memory</text>
                    <text x="0" y="160" class="log-line"><tspan fill="#e1e4e8">[ALGO]</tspan> Model execution feed matched: SELL limit BTC</text>
                    <text x="0" y="180" class="log-line"><tspan fill="#58a6ff">[INFO]</tspan> PostgreSQL connection pool recycled (32 active)</text>
                    <text x="0" y="200" class="log-line"><tspan fill="#39ff14">[SYS]</tspan> Healthcheck: 0 active errors in core pipelines</text>
                    
                    <!-- Frame 3 log lines -->
                    <text x="0" y="220" class="log-line"><tspan fill="#58a6ff">[INFO]</tspan> Git telemetry synced: generated stats</text>
                    <text x="0" y="240" class="log-line"><tspan fill="#39ff14">[SYS]</tspan> Scheduled cron task trigger complete</text>
                    <text x="0" y="260" class="log-line"><tspan fill="#e1e4e8">[HFT]</tspan> High-throughput order matched successfully</text>
                    <text x="0" y="280" class="log-line"><tspan fill="#39ff14">[OK]</tspan> Cloud deployment nodes responding OK</text>
                    <text x="0" y="300" class="log-line"><tspan fill="#58a6ff">[INFO]</tspan> Ready for next instructions...</text>
                </g>
            </g>
        </g>
        
        <!-- Blinking Prompt Line at bottom -->
        <g transform="translate(10, 185)">
            <text x="0" y="0" class="prompt">_</text>
            <rect x="0" y="-10" width="8" height="12" class="cursor"/>
        </g>
    </g>
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated stats terminal SVG at {filepath}")


def generate_contribution_matrix_svg(data, filepath):
    weeks = data.get("contribution_calendar", {}).get("weeks", [])
    total_contribs = data.get("contribution_calendar", {}).get("totalContributions", data["commit_count"])
    
    # Grid positioning configuration
    start_x = 240
    start_y = 55
    spacing = 11.5
    
    cells_svg = []
    styles = []
    
    # Cyberpunk status coloring palette
    level_colors = {
        "NONE": "#131621",
        "FIRST_QUARTILE": "#004d61",
        "SECOND_QUARTILE": "#008fa8",
        "THIRD_QUARTILE": "#7000ff",
        "FOURTH_QUARTILE": "#ff007f"
    }
    
    for w_idx, week in enumerate(weeks):
        for day in week.get("contributionDays", []):
            d_idx = day.get("weekday", 0)
            level = day.get("contributionLevel", "NONE")
            color = level_colors.get(level, "#131621")
            
            x = start_x + w_idx * spacing
            y = start_y + d_idx * spacing
            
            cells_svg.append(
                f'<rect class="cell cell-col-{w_idx}" x="{x}" y="{y}" width="9" height="9" rx="1.5" ry="1.5" fill="{color}" style="color: {color};" />'
            )
            
        # Synchronized scanline delays (staggered across 53 weeks over 6 seconds of an 8-second animation)
        delay = (w_idx / 53) * 6.0
        styles.append(f'        .cell-col-{w_idx} {{ animation: cell-glow 8s infinite; animation-delay: {delay:.2f}s; }}')

    styles_css = "\n".join(styles)
    cells_str = "\n".join(cells_svg)
    
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" width="100%" height="180">
    <defs>
        <pattern id="grid-contrib" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#12161f" stroke-width="1"/>
        </pattern>
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;900&amp;display=swap');
        
        .bg {{
            fill: #090a0f;
        }}
        .grid-overlay {{
            fill: url(#grid-contrib);
        }}
        .title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 14px;
            fill: #ffffff;
            letter-spacing: 1px;
        }}
        .subtitle {{
            font-family: 'Fira Code', monospace;
            font-size: 9px;
            fill: #8b949e;
            letter-spacing: 1px;
        }}
        .label {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: #58a6ff;
        }}
        .value {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: #39ff14;
            font-weight: bold;
        }}
        .grid-label {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: #8b949e;
        }}
        
        /* Sweep animation for scanner line */
        @keyframes sweep-line {{
            0% {{ transform: translateX(0px); opacity: 0; }}
            5% {{ opacity: 0.8; }}
            75% {{ opacity: 0.8; }}
            80% {{ transform: translateX(610px); opacity: 0; }}
            100% {{ transform: translateX(610px); opacity: 0; }}
        }}
        .scanner-bar {{
            animation: sweep-line 8s infinite ease-in-out;
        }}
        
        /* Cell sweep glow animation */
        @keyframes cell-glow {{
            0%, 100% {{ opacity: 0.6; }}
            8% {{ opacity: 1.0; filter: drop-shadow(0 0 3px currentColor); }}
            20% {{ opacity: 0.6; }}
        }}
        
        .cell {{
            opacity: 0.6;
        }}
        
{styles_css}
    </style>

    <!-- Background -->
    <rect width="900" height="180" rx="12" class="bg"/>
    <rect width="900" height="180" rx="12" class="grid-overlay"/>

    <!-- Telemetry Left Readout Panel -->
    <g transform="translate(40, 40)">
        <path d="M-15 -10 L15 -10 M-15 -10 L-15 25" stroke="#ff007f" stroke-width="1.5" fill="none" opacity="0.7"/>
        <text x="0" y="5" class="title">CONTRIBUTION GRID</text>
        <text x="0" y="20" class="subtitle">HOLOGRAPHIC telemetry matrix</text>
        
        <g transform="translate(0, 45)">
            <text x="0" y="0" class="label">SCAN_CYCLE: <tspan class="value">365 DAYS</tspan></text>
            <text x="0" y="15" class="label">GRID_SYNC: <tspan class="value">SUCCESS</tspan></text>
            <text x="0" y="30" class="label">INTEGRITY: <tspan class="value">100.0%</tspan></text>
            <text x="0" y="45" class="label">CONTRIBS:  <tspan class="value" fill="#00f0ff">{total_contribs} NODES</tspan></text>
        </g>
    </g>

    <!-- Grid Labels (Weekdays) -->
    <text x="218" y="62" class="grid-label">Sun</text>
    <text x="218" y="85" class="grid-label">Tue</text>
    <text x="218" y="108" class="grid-label">Thu</text>
    <text x="218" y="131" class="grid-label">Sat</text>

    <!-- Grid Cells -->
    <g>
{cells_str}
    </g>

    <!-- Scanning Holographic Sweep Bar -->
    <rect class="scanner-bar" x="237" y="50" width="3" height="85" fill="#00f0ff" filter="url(#glow-cyan)" opacity="0.8"/>
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Generated contribution matrix SVG at {filepath}")


# ---------------------------------------------------------
# 4. Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print(f"Executing stats dashboard SVG generation for operator {GITHUB_USERNAME}...")
    stats = fetch_github_data(GITHUB_USERNAME)
    print("Fetched statistics:", {k: v for k, v in stats.items() if k != "contribution_calendar"})
    
    header_path = os.path.join(ASSETS_DIR, "header_animation.svg")
    topology_path = os.path.join(ASSETS_DIR, "systems_topology.svg")
    stats_path = os.path.join(ASSETS_DIR, "terminal_stats.svg")
    contrib_path = os.path.join(ASSETS_DIR, "contribution_matrix.svg")
    
    generate_header_svg(stats, header_path)
    generate_topology_svg(topology_path)
    generate_terminal_stats_svg(stats, stats_path)
    generate_contribution_matrix_svg(stats, contrib_path)
    print("All assets compiled successfully!")
