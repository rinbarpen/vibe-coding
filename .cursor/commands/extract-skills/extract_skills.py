import os
import re
import argparse
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parents[3]
ANNOTATIONS_PATH = WORKSPACE_ROOT / "skills" / "ANNOTATIONS.md"

def parse_annotations(file_path):
    if not file_path.exists():
        return []
    
    content = file_path.read_text(encoding="utf-8")
    # Split by skill headers (### Name)
    skill_sections = re.split(r'\n###\s+', content)
    
    skills = []
    for section in skill_sections[1:]:  # Skip the part before the first skill
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        name = lines[0].strip()
        path = ""
        description = ""
        usage = ""
        
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("- **路径**:"):
                path = line.replace("- **路径**:", "").strip().strip('`')
            elif line.startswith("- **简介**:"):
                description = line.replace("- **简介**:", "").strip()
            elif line.startswith("- **使用场景**:"):
                usage = line.replace("- **使用场景**:", "").strip()
        
        skills.append({
            "name": name,
            "path": path,
            "description": description,
            "usage": usage,
            "full_text": f"{name} {description} {usage}".lower()
        })
    
    return skills

def calculate_score(skill, query_words):
    score = 0
    matched_words = []
    full_text = skill["full_text"]
    
    for word in query_words:
        if word in full_text:
            # Simple scoring: count occurrences or just existence
            # We can give more weight to name matches or usage matches
            weight = 1
            if word in skill["name"].lower():
                weight = 3
            elif word in skill["usage"].lower():
                weight = 2
                
            score += weight
            matched_words.append(word)
            
    return score, matched_words

def main():
    parser = argparse.ArgumentParser(description="Extract relevant skills based on task description.")
    parser.add_argument("query", type=str, help="Task description or keywords")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of skills to return")
    args = parser.parse_args()
    
    if not ANNOTATIONS_PATH.exists():
        print(f"Error: {ANNOTATIONS_PATH} not found. Please run /annotate-skills-mcp first.")
        return

    skills = parse_annotations(ANNOTATIONS_PATH)
    query = args.query.lower()
    # Simple tokenization
    query_words = [w for w in re.split(r'\W+', query) if len(w) > 1]
    
    scored_skills = []
    for skill in skills:
        score, matched = calculate_score(skill, query_words)
        if score > 0:
            scored_skills.append((score, matched, skill))
            
    # Sort by score descending
    scored_skills.sort(key=lambda x: x[0], reverse=True)
    
    top_skills = scored_skills[:args.limit]
    
    if not top_skills:
        print(f"未找到与 '{args.query}' 相关的技能。")
        return
        
    print(f"## 推荐的 Skills (基于: {args.query})\n")
    for i, (score, matched, skill) in enumerate(top_skills, 1):
        # Calculate a pseudo-percentage for display
        # Max possible score for this query
        max_score = sum(3 if w in skill["name"].lower() else 1 for w in query_words) # simplified
        rel = min(100, int((score / (len(query_words) * 2)) * 100)) if query_words else 0
        
        print(f"### {i}. {skill['name']} (相关性: {rel}%)")
        print(f"- **路径**: `{skill['path']}`")
        print(f"- **简介**: {skill['description']}")
        if skill['usage'] and skill['usage'] != "见简介":
            print(f"- **使用场景**: {skill['usage']}")
        print(f"- **匹配关键词**: {', '.join(set(matched))}")
        print()

if __name__ == "__main__":
    main()
