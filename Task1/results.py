import json
import os

def analyze_scores(filename="results.jsonl"):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run the main script first.")
        return

    total_entries = 0
    high_scores = 0
    score_distribution = {0.1: 0, 0.3: 0, 0.7: 0, 0.9: 0}

    with open(filename, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                score = data.get("score")
                
                if score is not None:
                    total_entries += 1
                    
                    # Track distribution
                    score_distribution[score] = score_distribution.get(score, 0) + 1
                    
                    # Count targets (0.7 to 0.9)
                    if 0.7 <= score <= 0.9:
                        high_scores += 1
            except json.JSONDecodeError:
                continue

    if total_entries == 0:
        print("No valid results found in the file.")
        return

    percentage = (high_scores / total_entries) * 100

    print("-" * 30)
    print(f"RECAPTCHA V3 ANALYSIS")
    print("-" * 30)
    print(f"Total Successful Solves: {total_entries}")
    print(f"Scores in 0.7 - 0.9 Range: {high_scores}")
    print(f"Current Success Rate: {percentage:.2f}%")
    print("-" * 30)
    print("Full Distribution:")
    for s in sorted(score_distribution.keys()):
        count = score_distribution[s]
        perc = (count / total_entries) * 100
        print(f" Score {s}: {count} ({perc:.1f}%)")
    print("-" * 30)
    
    if percentage >= 15:
        print("✅ Goal Met: You are above the 15% threshold.")
    else:
        print("❌ Goal Not Met: Success rate is below 15%.")

if __name__ == "__main__":
    analyze_scores()