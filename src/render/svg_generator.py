import os
from datetime import datetime

class SvgGenerator:
    def __init__(self, data, theme):
        self.data = data
        self.theme = theme
        
    def generate_all(self, assets_dir="assets"):
        os.makedirs(assets_dir, exist_ok=True)
        
        self.generate_git_telemetry_svg(os.path.join(assets_dir, "git_telemetry.svg"))
        self.generate_kubernetes_console_svg(os.path.join(assets_dir, "kubernetes_console.svg"))
        self.generate_stats_dashboard_svg(os.path.join(assets_dir, "stats_dashboard.svg"))
        self.generate_contribution_matrix_svg(os.path.join(assets_dir, "contribution_matrix.svg"))
        
    def generate_git_telemetry_svg(self, filepath):
        c = self.theme
        commit_types = self.data.get("commit_types", {})
        
        # Extract values
        feat = commit_types.get("features", 0)
        perf = commit_types.get("performance", 0)
        fix = commit_types.get("bugfixes", 0)
        devops = commit_types.get("devops", 0)
        refactor = commit_types.get("refactoring", 0)
        docs = commit_types.get("documentation", 0)
        
        # Calculate coordinate lengths for progress bars (max width 180)
        w_feat = int((feat / 100) * 180)
        w_perf = int((perf / 100) * 180)
        w_fix = int((fix / 100) * 180)
        w_devops = int((devops / 100) * 180)
        w_refactor = int((refactor / 100) * 180)
        
        svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="100%" height="260">
    <defs>
        <pattern id="grid-tel" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="{c.get("grid")}" stroke-width="1"/>
        </pattern>
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="glow-pink" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <linearGradient id="gradient-title" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{c.get("primary")}"/>
            <stop offset="50%" stop-color="{c.get("accent")}"/>
            <stop offset="100%" stop-color="{c.get("secondary")}"/>
        </linearGradient>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;900&amp;display=swap');
        
        .bg {{ fill: {c.get("bg")}; }}
        .grid-overlay {{ fill: url(#grid-tel); }}
        
        .title {{
            font-family: 'Outfit', system-ui, sans-serif;
            font-weight: 900;
            font-size: 40px;
            fill: url(#gradient-title);
            letter-spacing: 2px;
        }}
        .subtitle {{
            font-family: 'Fira Code', monospace;
            font-size: 13px;
            fill: {c.get("text_muted")};
            letter-spacing: 2px;
        }}
        .section-hdr {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 13px;
            fill: {c.get("text_primary")};
            letter-spacing: 1px;
        }}
        
        /* Bar chart fonts */
        .bar-label {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("text_muted")};
        }}
        .bar-value {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("primary")};
            font-weight: bold;
        }}
        
        .pill-label {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("text_blue")};
        }}
        
        @keyframes rotate-hud {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        .hud-gear {{
            transform-origin: 430px 130px;
            animation: rotate-hud 25s linear infinite;
        }}
        
        @keyframes status-blink {{
            0%, 100% {{ fill: {c.get("status_ok")}; filter: drop-shadow(0 0 2px {c.get("status_ok")}); }}
            50% {{ fill: {c.get("grid_light")}; filter: none; }}
        }}
        .status-dot {{
            animation: status-blink 2s infinite;
        }}
    </style>

    <rect width="900" height="260" rx="12" class="bg"/>
    <rect width="900" height="260" rx="12" class="grid-overlay"/>

    <!-- Decorative HUD Rotating Rings -->
    <g class="hud-gear" opacity="0.15">
        <circle cx="430" cy="130" r="70" fill="none" stroke="{c.get("accent")}" stroke-width="1.5" stroke-dasharray="10 8"/>
        <circle cx="430" cy="130" r="55" fill="none" stroke="{c.get("primary")}" stroke-width="1" stroke-dasharray="4 4"/>
    </g>

    <!-- Left Frame: Developer Credentials -->
    <g transform="translate(60, 65)">
        <path d="M-20 -15 L30 -15 M-20 -15 L-20 30" stroke="{c.get("secondary")}" stroke-width="2" fill="none" opacity="0.8"/>
        <text x="0" y="20" class="title">ABHINANDAN NAIK</text>
        <text x="0" y="45" class="subtitle">BACKEND ENGINEER // DEVSECOPS PIPELINES</text>
        
        <!-- Live Status Row -->
        <g transform="translate(0, 80)">
            <rect x="0" y="0" width="130" height="24" rx="12" fill="{c.get("bg_terminal")}" stroke="{c.get("grid")}" stroke-width="1"/>
            <circle cx="15" cy="12" r="4.5" class="status-dot"/>
            <text x="28" y="16" class="pill-label">PIPELINE: <tspan fill="{c.get("status_ok")}" font-weight="bold">ACTIVE</tspan></text>
            
            <rect x="145" y="0" width="135" height="24" rx="12" fill="{c.get("bg_terminal")}" stroke="{c.get("grid")}" stroke-width="1"/>
            <circle cx="160" cy="12" r="4" fill="{c.get("primary")}" filter="url(#glow-cyan)"/>
            <text x="173" y="16" class="pill-label">THEME: <tspan fill="{c.get("primary")}" font-weight="bold">{c.theme_name.upper()}</tspan></text>
        </g>
    </g>

    <!-- Right Frame: Conventional Commit Telemetry -->
    <g transform="translate(540, 45)">
        <rect x="0" y="0" width="300" height="170" fill="{c.get("bg_terminal")}" stroke="{c.get("grid")}" stroke-width="1.5" rx="8" opacity="0.8"/>
        
        <text x="20" y="25" class="section-hdr">ENGINEERING COMMITS TELEMETRY</text>
        
        <!-- Progress Bars representing conventional commits -->
        <g transform="translate(20, 45)">
            <!-- Features -->
            <text x="0" y="10" class="bar-label">Features (feat)</text>
            <rect x="130" y="2" width="100" height="7" rx="3.5" fill="{c.get("grid")}" />
            <rect x="130" y="2" width="{max(int(feat), 5)}" height="7" rx="3.5" fill="{c.get("primary")}" filter="url(#glow-cyan)"/>
            <text x="240" y="10" class="bar-value">{feat}%</text>
            
            <!-- Bugfixes -->
            <text x="0" y="30" class="bar-label">Bugfixes (fix)</text>
            <rect x="130" y="22" width="100" height="7" rx="3.5" fill="{c.get("grid")}" />
            <rect x="130" y="22" width="{max(int(fix), 5)}" height="7" rx="3.5" fill="{c.get("status_ok")}" />
            <text x="240" y="30" class="bar-value" fill="{c.get("status_ok")}">{fix}%</text>
            
            <!-- Performance -->
            <text x="0" y="50" class="bar-label">Performance (perf)</text>
            <rect x="130" y="42" width="100" height="7" rx="3.5" fill="{c.get("grid")}" />
            <rect x="130" y="42" width="{max(int(perf), 5)}" height="7" rx="3.5" fill="{c.get("secondary")}" filter="url(#glow-pink)"/>
            <text x="240" y="50" class="bar-value" fill="{c.get("secondary")}">{perf}%</text>

            <!-- DevOps -->
            <text x="0" y="70" class="bar-label">DevOps (ci/cd)</text>
            <rect x="130" y="62" width="100" height="7" rx="3.5" fill="{c.get("grid")}" />
            <rect x="130" y="62" width="{max(int(devops), 5)}" height="7" rx="3.5" fill="{c.get("accent")}" />
            <text x="240" y="70" class="bar-value" fill="{c.get("accent")}">{devops}%</text>

            <!-- Refactoring -->
            <text x="0" y="90" class="bar-label">Refactoring (refac)</text>
            <rect x="130" y="82" width="100" height="7" rx="3.5" fill="{c.get("grid")}" />
            <rect x="130" y="82" width="{max(int(refactor), 5)}" height="7" rx="3.5" fill="{c.get("status_warn")}" />
            <text x="240" y="90" class="bar-value" fill="{c.get("status_warn")}">{refactor}%</text>
        </g>
    </g>
</svg>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_template)
        print(f"Generated Git telemetry SVG at {filepath}")
        
    def generate_kubernetes_console_svg(self, filepath):
        c = self.theme
        
        svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" width="100%" height="420">
    <defs>
        <pattern id="grid-k8s" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{c.get("grid")}" stroke-width="1"/>
        </pattern>
        <filter id="glow-k8s-cyan" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        <filter id="glow-k8s-pink" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;900&amp;display=swap');
        
        .bg {{ fill: {c.get("bg")}; }}
        .grid-overlay {{ fill: url(#grid-k8s); }}
        
        .panel-title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 14px;
            fill: #ffffff;
            letter-spacing: 1.5px;
        }}
        
        /* Node & Namespace labels */
        .ns-box {{
            fill: {c.get("bg_terminal")};
            stroke: {c.get("grid")};
            stroke-width: 1.5;
            opacity: 0.85;
        }}
        .ns-title {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("text_muted")};
            font-weight: bold;
        }}
        .pod-box {{
            fill: {c.get("bg")};
            stroke: {c.get("grid_light")};
            stroke-width: 1;
        }}
        .pod-title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 11px;
            fill: #ffffff;
        }}
        .pod-metrics {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: {c.get("text_muted")};
        }}
        
        /* Network Packet Flow animations */
        @keyframes flow-k8s {{
            to {{
                stroke-dashoffset: -40;
            }}
        }}
        .k8s-link {{
            stroke-width: 1.5;
            fill: none;
            stroke-dasharray: 5 8;
            animation: flow-k8s 2.5s linear infinite;
        }}
        .link-cyan {{
            stroke: {c.get("primary")};
            filter: drop-shadow(0 0 1px {c.get("primary")});
        }}
        .link-pink {{
            stroke: {c.get("secondary")};
            filter: drop-shadow(0 0 1px {c.get("secondary")});
        }}
        .link-static {{
            stroke: {c.get("grid")};
            stroke-width: 1.5;
            fill: none;
        }}
        
        /* Pod state pulsing indicators */
        @keyframes state-pulse {{
            0%, 100% {{ opacity: 0.4; fill: {c.get("status_ok")}; }}
            50% {{ opacity: 1.0; fill: {c.get("status_ok")}; filter: drop-shadow(0 0 3px {c.get("status_ok")}); }}
        }}
        .status-pulse {{
            animation: state-pulse 2s infinite ease-in-out;
        }}
    </style>

    <rect width="900" height="420" rx="12" class="bg"/>
    <rect width="900" height="420" rx="12" class="grid-overlay"/>

    <!-- Section Title -->
    <g transform="translate(40, 35)">
        <path d="M-10 -10 L15 -10 M-10 -10 L-10 15" stroke="{c.get("secondary")}" stroke-width="2" fill="none"/>
        <text x="10" y="5" class="panel-title">KUBERNETES MICROSERVICES TOPO-FABRIC</text>
    </g>

    <!-- Network connection paths (Behind namespace panels) -->
    <!-- Ingress to Core -->
    <path d="M 180 200 L 320 150" class="link-static"/>
    <path d="M 180 200 L 320 150" class="k8s-link link-pink"/>

    <path d="M 180 200 L 320 250" class="link-static"/>
    <path d="M 180 200 L 320 250" class="k8s-link link-pink"/>

    <!-- Core to Messaging -->
    <path d="M 460 150 L 560 200" class="link-static"/>
    <path d="M 460 150 L 560 200" class="k8s-link link-cyan"/>

    <path d="M 460 250 L 560 200" class="link-static"/>
    <path d="M 460 250 L 560 200" class="k8s-link link-cyan"/>

    <!-- Messaging to Database -->
    <path d="M 700 200 L 800 200" class="link-static"/>
    <path d="M 700 200 L 800 200" class="k8s-link link-cyan"/>


    <!-- 1. Namespace Panel: Ingress Controller (Left) -->
    <g transform="translate(40, 110)">
        <rect width="140" height="180" rx="6" class="ns-box"/>
        <text x="15" y="20" class="ns-title">ns: ingress-routing</text>
        
        <!-- Pod: Ingress Gateway -->
        <g transform="translate(10, 35)">
            <rect width="120" height="125" rx="4" class="pod-box"/>
            <!-- Status dot -->
            <circle cx="20" cy="20" r="4.5" class="status-pulse"/>
            <text x="35" y="24" class="pod-title">ingress-gtw</text>
            
            <g transform="translate(15, 45)" class="pod-metrics">
                <text x="0" y="15">STATUS: Running</text>
                <text x="0" y="30">CPU: 0.8%</text>
                <text x="0" y="45">MEM: 82MB</text>
                <text x="0" y="60">RESTARTS: 0</text>
            </g>
        </g>
    </g>


    <!-- 2. Namespace Panel: Trading Core (Center-Left) -->
    <g transform="translate(320, 70)">
        <rect width="200" height="270" rx="6" class="ns-box"/>
        <text x="15" y="20" class="ns-title">ns: execution-core</text>
        
        <!-- Pod 1: Spring Core -->
        <g transform="translate(15, 35)">
            <rect width="170" height="100" rx="4" class="pod-box"/>
            <circle cx="20" cy="20" r="4.5" class="status-pulse"/>
            <text x="35" y="24" class="pod-title">spring-api-serv</text>
            <g transform="translate(15, 40)" class="pod-metrics">
                <text x="0" y="12">STATUS: Running</text>
                <text x="0" y="24">CPU: 1.4% // MEM: 256MB</text>
                <text x="0" y="36">NET_IN: 124kb/s</text>
            </g>
        </g>

        <!-- Pod 2: Trading Engine -->
        <g transform="translate(15, 150)">
            <rect width="170" height="100" rx="4" class="pod-box"/>
            <circle cx="20" cy="20" r="4.5" class="status-pulse"/>
            <text x="35" y="24" class="pod-title">trading-engine</text>
            <g transform="translate(15, 40)" class="pod-metrics">
                <text x="0" y="12">STATUS: Running</text>
                <text x="0" y="24">CPU: 4.8% // MEM: 196MB</text>
                <text x="0" y="36">ALGO_THREADS: 32</text>
            </g>
        </g>
    </g>


    <!-- 3. Namespace Panel: Event Brokers (Center-Right) -->
    <g transform="translate(560, 110)">
        <rect width="140" height="180" rx="6" class="ns-box"/>
        <text x="15" y="20" class="ns-title">ns: event-piping</text>
        
        <!-- Pod: Kafka Bus -->
        <g transform="translate(10, 35)">
            <rect width="120" height="125" rx="4" class="pod-box"/>
            <circle cx="20" cy="20" r="4.5" class="status-pulse"/>
            <text x="35" y="24" class="pod-title">kafka-cluster</text>
            
            <g transform="translate(15, 45)" class="pod-metrics">
                <text x="0" y="15">STATUS: Running</text>
                <text x="0" y="30">CPU: 2.1%</text>
                <text x="0" y="45">MEM: 512MB</text>
                <text x="0" y="60">LAG: 0.00ms</text>
            </g>
        </g>
    </g>


    <!-- 4. Namespace Panel: Storage (Right) -->
    <g transform="translate(740, 110)">
        <rect width="120" height="180" rx="6" class="ns-box"/>
        <text x="15" y="20" class="ns-title">ns: db-storage</text>
        
        <!-- Pod: Postgres DB -->
        <g transform="translate(10, 35)">
            <rect width="100" height="125" rx="4" class="pod-box"/>
            <circle cx="20" cy="20" r="4.5" class="status-pulse"/>
            <text x="35" y="24" class="pod-title">postgres-db</text>
            
            <g transform="translate(12, 45)" class="pod-metrics">
                <text x="0" y="15">STATUS: Running</text>
                <text x="0" y="30">CONNS: 24/100</text>
                <text x="0" y="45">HIT_RATE: 99.4%</text>
                <text x="0" y="60">SIZE: 1.2GB</text>
            </g>
        </g>
    </g>
</svg>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_template)
        print(f"Generated Kubernetes console SVG at {filepath}")
        
    def generate_stats_dashboard_svg(self, filepath):
        c = self.theme
        joined_year = self.data["joined_year"]
        repos = self.data["repo_count"]
        stars = self.data["star_count"]
        commits = self.data["commit_count"]
        followers = self.data["followers"]
        
        lc = self.data.get("leetcode", {"easy": 0, "medium": 0, "hard": 0, "total": 0})
        lc_total = lc.get("total", 0)
        lc_easy = lc.get("easy", 0)
        lc_medium = lc.get("medium", 0)
        lc_hard = lc.get("hard", 0)
        
        # Calculate lengths of progress bars for LeetCode (max width 160)
        max_solved = max(lc_total, 1)
        w_easy = int((lc_easy / max_solved) * 160) if lc_total > 0 else 30
        w_med = int((lc_medium / max_solved) * 160) if lc_total > 0 else 60
        w_hard = int((lc_hard / max_solved) * 160) if lc_total > 0 else 15
        
        svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="100%" height="320">
    <defs>
        <pattern id="grid-db" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{c.get("grid")}" stroke-width="1"/>
        </pattern>
        <linearGradient id="db-hdr-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{c.get("grid_light")}"/>
            <stop offset="100%" stop-color="{c.get("bg_terminal")}"/>
        </linearGradient>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&amp;display=swap');
        
        .bg {{ fill: {c.get("bg_terminal")}; }}
        .grid-overlay {{ fill: url(#grid-db); }}
        
        .db-hdr {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            fill: {c.get("text_muted")};
            font-weight: bold;
        }}
        .db-title {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: {c.get("secondary")};
            font-weight: bold;
        }}
        
        .stat-lbl {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: {c.get("text_primary")};
        }}
        .stat-number {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: {c.get("text_blue")};
            font-weight: bold;
        }}
        
        .lc-title {{
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            fill: {c.get("primary")};
            font-weight: bold;
        }}
        .lc-lbl {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("text_muted")};
        }}
        
        @keyframes scroll-logs {{
            0%, 15% {{ transform: translateY(0px); }}
            20%, 35% {{ transform: translateY(-18px); }}
            40%, 55% {{ transform: translateY(-36px); }}
            60%, 75% {{ transform: translateY(-54px); }}
            80%, 95% {{ transform: translateY(-72px); }}
            100% {{ transform: translateY(-90px); }}
        }}
        .log-scroller {{
            animation: scroll-logs 14s steps(5) infinite;
        }}
        .log-row {{
            font-family: 'Fira Code', monospace;
            font-size: 10px;
            fill: {c.get("text_muted")};
            white-space: nowrap;
        }}
    </style>

    <rect width="900" height="320" rx="8" class="bg"/>
    <rect width="900" height="320" rx="8" class="grid-overlay"/>
    <rect width="898" height="318" x="1" y="1" rx="8" fill="none" stroke="{c.get("grid")}" stroke-width="1.5"/>

    <!-- Header bar -->
    <path d="M 1 8 L 1 30 L 899 30 L 899 8 A 7 7 0 0 0 892 1 L 8 1 A 7 7 0 0 0 1 8 Z" fill="url(#db-hdr-grad)" stroke="{c.get("grid")}" stroke-width="1"/>
    <circle cx="20" cy="15" r="5" fill="{c.get("secondary")}"/>
    <circle cx="36" cy="15" r="5" fill="{c.get("status_warn")}"/>
    <circle cx="52" cy="15" r="5" fill="{c.get("status_ok")}"/>
    <text x="450" y="19" class="db-hdr" text-anchor="middle">abhinandan@systems-metrics:~ (profile_telemetry)</text>

    <!-- Content partition panels -->
    <g transform="translate(30, 60)">
        
        <!-- Left Panel: Core Dev Metrics -->
        <g>
            <text x="0" y="0" class="db-title">METRICS://CORE_INDEX</text>
            
            <g transform="translate(10, 25)">
                <text x="0" y="0" class="stat-lbl">USER_ID:</text>
                <text x="180" y="0" class="stat-number">AbhinandanNaik</text>

                <text x="0" y="24" class="stat-lbl">SYSTEM_UPTIME:</text>
                <text x="180" y="24" class="stat-number">{datetime.now().year - int(joined_year)} Years ({joined_year})</text>

                <text x="0" y="48" class="stat-lbl">REPOS_LOADED:</text>
                <text x="180" y="48" class="stat-number">{repos} Active Clusters</text>

                <text x="0" y="72" class="stat-lbl">SYNC_COMMITS:</text>
                <text x="180" y="72" class="stat-number" fill="{c.get("status_ok")}">{commits} Transports</text>

                <text x="0" y="96" class="stat-lbl">RATING_REPUTATION:</text>
                <text x="180" y="96" class="stat-number">{stars} Stars // {followers} Followers</text>
            </g>
        </g>

        <!-- Divider -->
        <line x1="420" y1="-15" x2="420" y2="230" stroke="{c.get("grid")}" stroke-width="1.5"/>

        <!-- Right Panel: LeetCode Algorithmic stats -->
        <g transform="translate(450, 0)">
            <text x="0" y="0" class="lc-title">METRICS://ALGO_SOLVED</text>
            <text x="350" y="0" class="stat-number" fill="{c.get("status_ok")}">{lc_total} Solved</text>
            
            <g transform="translate(10, 25)">
                <!-- Easy -->
                <text x="0" y="10" class="lc-lbl">Easy Problems</text>
                <rect x="140" y="2" width="180" height="7" rx="3.5" fill="{c.get("grid")}" />
                <rect x="140" y="2" width="{max(w_easy, 5)}" height="7" rx="3.5" fill="{c.get("status_ok")}" />
                <text x="330" y="10" class="stat-number">{lc_easy}</text>

                <!-- Medium -->
                <text x="0" y="34" class="lc-lbl">Medium Problems</text>
                <rect x="140" y="26" width="180" height="7" rx="3.5" fill="{c.get("grid")}" />
                <rect x="140" y="26" width="{max(w_med, 5)}" height="7" rx="3.5" fill="{c.get("status_warn")}" />
                <text x="330" y="34" class="stat-number">{lc_medium}</text>

                <!-- Hard -->
                <text x="0" y="58" class="lc-lbl">Hard Problems</text>
                <rect x="140" y="50" width="180" height="7" rx="3.5" fill="{c.get("grid")}" />
                <rect x="140" y="50" width="{max(w_hard, 5)}" height="7" rx="3.5" fill="{c.get("secondary")}" />
                <text x="330" y="58" class="stat-number">{lc_hard}</text>
            </g>

            <!-- Rolling algorithmic logs buffer -->
            <g transform="translate(10, 110)">
                <line x1="-10" y1="0" x2="380" y2="0" stroke="{c.get("grid")}" stroke-width="1"/>
                <g clip-path="url(#lc-log-clip)" transform="translate(0, 10)">
                    <clipPath id="lc-log-clip">
                        <rect x="0" y="0" width="380" height="90"/>
                    </clipPath>
                    <g class="log-scroller">
                        <text x="0" y="10" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Binary search optimizer: completed (8ms)</text>
                        <text x="0" y="28" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Dijkstra routing nodes traversal: OK</text>
                        <text x="0" y="46" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Matrix chain dynamic planning complete</text>
                        <text x="0" y="64" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Fast Fourier algorithm signal parsing OK</text>
                        <text x="0" y="82" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> LRU cache page eviction test: executed</text>
                        
                        <text x="0" y="100" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> AVL self-balancing tree rotate operation: OK</text>
                        <text x="0" y="118" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Max heap priority queue pop complexity: verified</text>
                        <text x="0" y="136" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> A* heuristics navigation grid: path calculated</text>
                        <text x="0" y="154" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Rabin-Karp substring hashing pattern matching: OK</text>
                        <text x="0" y="172" class="log-row"><tspan fill="{c.get("status_ok")}">[AC]</tspan> Thread pool executor concurrency threshold: verified</text>
                    </g>
                </g>
            </g>
        </g>
    </g>
</svg>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_template)
        print(f"Generated statistics dashboard SVG at {filepath}")
        
    def generate_contribution_matrix_svg(self, filepath):
        c = self.theme
        weeks = self.data.get("contribution_calendar", {}).get("weeks", [])
        total_contribs = self.data.get("contribution_calendar", {}).get("totalContributions", self.data["commit_count"])
        
        # Grid positioning configuration
        start_x = 240
        start_y = 55
        spacing = 11.5
        
        cells_svg = []
        styles = []
        
        # Color mapping configuration based on theme accent color tokens
        level_colors = {
            "NONE": c.get("grid"),
            "FIRST_QUARTILE": c.get("grid_light"),
            "SECOND_QUARTILE": c.get("accent"),
            "THIRD_QUARTILE": c.get("primary"),
            "FOURTH_QUARTILE": c.get("secondary")
        }
        
        for w_idx, week in enumerate(weeks):
            for day in week.get("contributionDays", []):
                d_idx = day.get("weekday", 0)
                level = day.get("contributionLevel", "NONE")
                color = level_colors.get(level, c.get("grid"))
                
                x = start_x + w_idx * spacing
                y = start_y + d_idx * spacing
                
                cells_svg.append(
                    f'<rect class="cell cell-col-{w_idx}" x="{x}" y="{y}" width="9" height="9" rx="1.5" ry="1.5" fill="{color}" style="color: {color};" />'
                )
                
            delay = (w_idx / 53) * 6.0
            styles.append(f'        .cell-col-{w_idx} {{ animation: cell-glow 8s infinite; animation-delay: {delay:.2f}s; }}')

        styles_css = "\n".join(styles)
        cells_str = "\n".join(cells_svg)
        
        svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" width="100%" height="180">
    <defs>
        <pattern id="grid-contrib" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="{c.get("grid")}" stroke-width="1"/>
        </pattern>
        <filter id="glow-contrib-primary" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=Outfit:wght@600;900&amp;display=swap');
        
        .bg {{ fill: {c.get("bg")}; }}
        .grid-overlay {{ fill: url(#grid-contrib); }}
        
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
            fill: {c.get("text_muted")};
            letter-spacing: 1px;
        }}
        .label {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: {c.get("text_blue")};
        }}
        .value {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: {c.get("status_ok")};
            font-weight: bold;
        }}
        .grid-label {{
            font-family: 'Fira Code', monospace;
            font-size: 8px;
            fill: {c.get("text_muted")};
        }}
        
        /* Sweep animation for scanner line */
        @keyframes sweep-line-contrib {{
            0% {{ transform: translateX(0px); opacity: 0; }}
            5% {{ opacity: 0.8; }}
            75% {{ opacity: 0.8; }}
            80% {{ transform: translateX(610px); opacity: 0; }}
            100% {{ transform: translateX(610px); opacity: 0; }}
        }}
        .scanner-bar {{
            animation: sweep-line-contrib 8s infinite ease-in-out;
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

    <rect width="900" height="180" rx="12" class="bg"/>
    <rect width="900" height="180" rx="12" class="grid-overlay"/>

    <!-- Telemetry Left Readout Panel -->
    <g transform="translate(40, 40)">
        <path d="M-15 -10 L15 -10 M-15 -10 L-15 25" stroke="{c.get("secondary")}" stroke-width="1.5" fill="none" opacity="0.7"/>
        <text x="0" y="5" class="title">CONTRIBUTION GRID</text>
        <text x="0" y="20" class="subtitle">HOLOGRAPHIC telemetry matrix</text>
        
        <g transform="translate(0, 45)">
            <text x="0" y="0" class="label">SCAN_CYCLE: <tspan class="value">365 DAYS</tspan></text>
            <text x="0" y="15" class="label">GRID_SYNC:  <tspan class="value">SUCCESS</tspan></text>
            <text x="0" y="30" class="label">INTEGRITY:  <tspan class="value">100.0%</tspan></text>
            <text x="0" y="45" class="label">CONTRIBS:   <tspan class="value" fill="{c.get("primary")}">{total_contribs} NODES</tspan></text>
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
    <rect class="scanner-bar" x="237" y="50" width="3" height="85" fill="{c.get("primary")}" filter="url(#glow-contrib-primary)" opacity="0.8"/>
</svg>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_template)
        print(f"Generated contribution matrix SVG at {filepath}")
