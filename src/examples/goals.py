"""Example goals for different agent paradigms and types combinations."""

from typing import Dict, List

# ReAct + ModelBasedReflex の組み合わせ用ゴール
REACT_MODEL_BASED_GOALS: Dict[str, Dict[str, str]] = {
    "task_management": {
        "title": "Task Management Assistant",
        "description": """あなたは私のタスク管理アシスタントです。以下のタスクを管理してください：
1. プロジェクトAのコード作成（優先度：高）
2. 週次レポートの作成（優先度：中）
3. チームミーティングの準備（優先度：中）
4. メールの返信（優先度：低）

各タスクの状態を追跡し、優先順位に基づいて次に取り組むべきタスクを提案してください。"""
    },
    "resource_management": {
        "title": "Resource Allocation Optimizer",
        "description": """開発チームのリソース配分を最適化してください。利用可能なリソース：
- 開発者3名（スキル：Python, JavaScript, DevOps）
- 残り時間：2週間
- 予算：限定的

以下のタスクに対してリソースを配分し、進捗を追跡してください：
1. フロントエンド開発
2. バックエンド API 実装
3. インフラストラクチャーのセットアップ"""
    },
    "problem_solving": {
        "title": "Performance Issue Resolver",
        "description": """以下のソフトウェア開発の問題を解決してください：
アプリケーションのパフォーマンスが低下しており、以下の症状が報告されています：
1. ページロードが遅い
2. データベースクエリのレスポンスが遅い
3. メモリ使用量が増加している

問題を分析し、解決策を提案・実装してください。"""
    },
    "learning_adaptation": {
        "title": "Adaptive Recommendation System",
        "description": """ユーザーの好みを学習し、カスタマイズされた推薦を行うアシスタントとして機能してください。
以下の情報を追跡し、学習してください：
1. ユーザーが選択したオプション
2. 拒否された推薦
3. 明示的なフィードバック

学習した情報を基に、より適切な推薦を行ってください。"""
    }
}

# 他のパラダイムとタイプの組み合わせ用のゴールもここに追加可能
# 例: REWOO_SIMPLE_REFLEX_GOALS, REACT_UTILITY_BASED_GOALS など

def get_available_goals(paradigm: str, agent_type: str) -> List[Dict[str, str]]:
    """Get available goals for the specified paradigm and agent type combination.
    
    Args:
        paradigm: The paradigm name (e.g., "react", "rewoo")
        agent_type: The agent type name (e.g., "model_based_reflex", "simple_reflex")
        
    Returns:
        List of available goals with their titles and descriptions
    """
    if paradigm.lower() == "react" and agent_type.lower() == "model_based_reflex":
        return [
            {"name": name, **goal}
            for name, goal in REACT_MODEL_BASED_GOALS.items()
        ]
    
    # 他のパラダイムとタイプの組み合わせに対するゴールの取得ロジックを追加可能
    
    return []

def get_goal_description(paradigm: str, agent_type: str, goal_name: str) -> str:
    """Get the description of a specific goal.
    
    Args:
        paradigm: The paradigm name
        agent_type: The agent type name
        goal_name: The name of the goal
        
    Returns:
        The goal description or None if not found
    """
    if paradigm.lower() == "react" and agent_type.lower() == "model_based_reflex":
        return REACT_MODEL_BASED_GOALS.get(goal_name, {}).get("description")
    
    return None 