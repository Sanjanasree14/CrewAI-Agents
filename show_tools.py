import sys
import os

# ✅ Append 'src' folder to sys.path so Python can find the real fact_checker module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(project_root)

# ✅ Now import
from fact_checker.crew import FactChecker

fc = FactChecker()

print("🔧 Tools used by the Crew:")
for tool in fc.tools:
    name = tool.__class__.__name__
    desc = getattr(tool, 'description', 'No description')
    print(f"✅ {name}: {desc}")
