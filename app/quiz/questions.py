# Quiz Questions
from app.models.user import QuizQuestion, PersonaType

QUIZ_QUESTIONS = [
    QuizQuestion(
        id=1, scene="meeting",
        question="\u4f1a\u8bae\u4e0a\u8001\u677f\u95ee\uff1a\u5927\u5bb6\u6709\u4ec0\u4e48\u95ee\u9898\u5417\uff1f",
        options=[
            {"text": "\u6ca1\u6709\u95ee\u9898\uff0c\u90fd\u5f88\u597d", "persona": "sha_seng"},
            {"text": "\u6211\u6709\u4e9b\u5efa\u8bae\u60f3\u8bf4", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u5148\u60f3\u60f3\u518d\u56de\u590d", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\u6709\u8da3\uff0c\u8fd9\u4f1a\u5f00\u5f97\u4e0d\u9519", "persona": "yue_yunpeng"},
            {"text": "\u95ee\u4e86\u4e5f\u767d\u95ee\uff0c\u6ca1\u4eba\u542c", "persona": "xiao_s"},
            {"text": "\u4eba\u751f\u5c31\u662f\u8fd9\u6837\uff0c\u4e0b\u73ed\u5427", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=2, scene="deadline",
        question="\u540c\u4e8b\u8bf4\uff1a\u8fd9\u4e2a\u4eca\u5929\u80fd\u5b8c\u6210\u5417\uff1f",
        options=[
            {"text": "\u597d\u7684\u597d\u7684\uff0c\u6ca1\u95ee\u9898\uff01", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e2a\u8fdb\u5ea6\u4e0d\u592a\u5408\u7406\u5427", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u770b\u770b\u65e5\u7a0b\u5b89\u6392", "persona": "zhen_huan"},
            {"text": "\u54ce\u5466\u558a\uff0c\u4f60\u8981\u547d\u554a\uff01", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u8ba4\u771f\u7684\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u5143\u6c14\u6d88\u8017\u5b8c\u5c31\u597d\uff0c\u4e0d\u7528\u6025", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=3, scene="feedback",
        question="\u8001\u677f\u5f53\u4f17\u6279\u8bc4\u4e86\u4f60\u7684\u5de5\u4f5c",
        options=[
            {"text": "\u8c22\u8c22\u8001\u677f\u6307\u6559\uff01", "persona": "sha_seng"},
            {"text": "\u6211\u4e0d\u5b8c\u5168\u540c\u610f\u8fd9\u4e2a\u8bc4\u4ef7", "persona": "hanzawa_naoki"},
            {"text": "\u611f\u8c22\u60a8\u7684\u53cd\u9988\uff0c\u6211\u4f1a\u6539\u8fdb", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u88ab\u6279\u4e86\u554a\uff0c\u6211\u5fc3\u91cc\u6709\u6570", "persona": "yue_yunpeng"},
            {"text": "\u5566\uff1f\u8bf7\u95ee\u6211\u54ea\u91cc\u505a\u5f97\u4e0d\u597d\uff1f", "persona": "xiao_s"},
            {"text": "\u75db\u82e6\u662f\u4eba\u751f\u7684\u5e38\u6001", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=4, scene="overtime",
        question="\u5468\u672b\u88ab\u8981\u6c42\u52a0\u73ed",
        options=[
            {"text": "\u597d\u7684\uff0c\u6211\u6765\u52a0\u73ed", "persona": "sha_seng"},
            {"text": "\u5468\u672b\u52a0\u73ed\u8fdd\u53cd\u52b3\u52a8\u6cd5", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u770b\u770b\u80fd\u4e0d\u80fd\u534f\u8c03\u4e00\u4e0b", "persona": "zhen_huan"},
            {"text": "\u6211\u7684\u5468\u672b\uff01\u4e0d\u884c\u554a\uff01", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u5728\u5f00\u73a9\u7b11\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u52a0\u73ed\u4e5f\u662f\u4e00\u79cd\u4f11\u606f\uff0c\u53cd\u6b63\u56de\u5bb6\u4e5f\u65e0\u804a", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=5, scene="credit",
        question="\u540c\u4e8b\u62a2\u4e86\u4f60\u7684\u529f\u52b3",
        options=[
            {"text": "\u6ca1\u4e8b\uff0c\u56e2\u961f\u6210\u679c\u6700\u91cd\u8981", "persona": "sha_seng"},
            {"text": "\u8fd9\u5176\u5b9e\u662f\u6211\u505a\u7684", "persona": "hanzawa_naoki"},
            {"text": "\u5f88\u9ad8\u5174\u9879\u76ee\u6210\u529f\u4e86", "persona": "zhen_huan"},
            {"text": "\u54ce\uff0c\u4f60\u771f\u725b\uff01\u4e0b\u6b21\u5e26\u5e26\u6211\uff01", "persona": "yue_yunpeng"},
            {"text": "\u6211\u60f3\u6211\u8033\u6735\u51fa\u95ee\u9898\u4e86", "persona": "xiao_s"},
            {"text": "\u4e16\u754c\u4e0a\u6ca1\u6709\u4ec0\u4e48\u662f\u771f\u6b63\u5c5e\u4e8e\u6211\u4eec\u7684", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=6, scene="lunch",
        question="\u540c\u4e8b\u95ee\u4f60\u4e2d\u5348\u5403\u4ec0\u4e48\uff0c\u7136\u540e\u8bf4\u4ed6\u4eec\u8981\u70b9\u5916\u5356\uff0c\u95ee\u4f60\u5403\u4ec0\u4e48",
        options=[
            {"text": "\u6211\u90fd\u884c\uff0c\u8ddf\u4f60\u4eec\u4e00\u8d77\u5403", "persona": "sha_seng"},
            {"text": "\u6211\u5df2\u7ecf\u5e26\u996d\u4e86\uff0c\u4e0d\u7528\u4e86\u8c22\u8c22", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u518d\u770b\u770b\u5427\uff0c\u7b49\u4f1a\u56de\u590d\u4f60", "persona": "zhen_huan"},
            {"text": "\u70b9\u5916\u5356\uff1f\u90a3\u6211\u53ef\u592a\u5f00\u5fc3\u4e86\uff01", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u4eec\u6bcf\u6b21\u90fd\u8fd9\u6837\uff0c\u6211\u5df2\u7ecf\u4e0d\u60f3\u8bf4\u4e86", "persona": "xiao_s"},
            {"text": "\u5403\u4ec0\u4e48\u4e0d\u91cd\u8981\uff0c\u80fd\u5403\u9971\u5c31\u884c", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=7, scene="chat",
        question="\u7fa4\u91cc\u6709\u4eba\u53d1\u4e86\u4e00\u4e2a\u5f88\u51b7\u7684\u7b11\u8bdd\uff0c\u5168\u573a\u5bc2\u9759",
        options=[
            {"text": "\u54c8\u54c8\uff0c\u8fd8\u884c\u8fd8\u884c\uff0c\u6211\u7b11\u4e86", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e2a\u65f6\u5019\u5c31\u4e0d\u8981\u8bf4\u8bdd\u4e86\u5427", "persona": "hanzawa_naoki"},
            {"text": "\u54c8\u54c8\uff0c\u4f60\u5f88\u6709\u610f\u601d\u5440", "persona": "zhen_huan"},
            {"text": "\u6211\u6765\u6362\u4e2a\uff01\u542c\u6211\u8bf4\u2026\u2026", "persona": "yue_yunpeng"},
            {"text": "\u5c4f\u5e55\u90fd\u5c34\u5c2c\u4e86\uff0c\u6211\u4e3a\u4f60\u5c34\u5c2c", "persona": "xiao_s"},
            {"text": "\u5c34\u5c2c\u662f\u793e\u4ea4\u7684\u5e38\u6001\uff0c\u4e0d\u7528\u5728\u610f", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=8, scene="leave",
        question="\u4f60\u60f3\u8bf7\u5047\uff0c\u4f46\u8001\u677f\u8bf4\u73b0\u5728\u5f88\u5fd9",
        options=[
            {"text": "\u597d\u7684\uff0c\u90a3\u6211\u518d\u7b49\u7b49", "persona": "sha_seng"},
            {"text": "\u6211\u5df2\u7ecf\u63d0\u524d\u5b89\u6392\u597d\u5de5\u4f5c\u4e86", "persona": "hanzawa_naoki"},
            {"text": "\u7406\u89e3\uff0c\u90a3\u6211\u770b\u770b\u5176\u4ed6\u65f6\u95f4", "persona": "zhen_huan"},
            {"text": "\u5fd9\u5230\u8fd9\u79cd\u7a0b\u5ea6\uff0c\u8001\u677f\u4e5f\u4e0d\u5bb9\u6613\u554a", "persona": "yue_yunpeng"},
            {"text": "\u6bcf\u6b21\u90fd\u5fd9\uff0c\u6211\u662f\u673a\u5668\u4eba\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u4eba\u751f\u82e6\u77ed\uff0c\u8be5\u4f11\u606f\u5c31\u4f11\u606f\u5427", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=9, scene="group",
        question="\u540c\u4e8b\u5728\u7fa4\u91cc @\u4f60\uff0c\u8ba9\u4f60\u5e2e\u5fd9\u505a\u4e00\u4e2a\u4e0d\u5c5e\u4e8e\u4f60\u7684\u4efb\u52a1",
        options=[
            {"text": "\u597d\u7684\uff0c\u6211\u6765\u770b\u770b", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e0d\u662f\u6211\u7684\u5de5\u4f5c\u8303\u56f4", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u624b\u5934\u6709\u70b9\u4e8b\uff0c\u4f60\u5148\u627e\u522b\u4eba\u5427", "persona": "zhen_huan"},
            {"text": "\u54ce\u5466\u558a\uff0c\u4f60\u8fd9\u662f\u770b\u4e0a\u6211\u4e86\u5440\uff01", "persona": "yue_yunpeng"},
            {"text": "\u4f60 @\u6211\u5c31\u662f\u8ba9\u6211\u5e72\u6d3b\uff1f", "persona": "xiao_s"},
            {"text": "\u5e2e\u4eba\u5bb6\u5c31\u662f\u5e2e\u81ea\u5df1\uff0c\u4e0d\u6025", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=10, scene="promotion",
        question="\u540c\u4e8b\u88ab\u63d0\u62d4\u4e86\uff0c\u4f46\u4f60\u89c9\u5f97\u4ed6\u80fd\u529b\u4e0d\u5982\u4f60",
        options=[
            {"text": "\u606d\u559c\u4f60\u554a\uff0c\u4ee5\u540e\u591a\u5173\u7167", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e2a\u7ed3\u679c\u6211\u65e0\u6cd5\u63a5\u53d7", "persona": "hanzawa_naoki"},
            {"text": "\u516c\u53f8\u7684\u51b3\u5b9a\u81ea\u7136\u6709\u5b83\u7684\u9053\u7406", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u90a3\u6211\u4ee5\u540e\u5c31\u9760\u4f60\u7167\u987e\u4e86\uff01", "persona": "yue_yunpeng"},
            {"text": "\u7b11\u6b7b\uff0c\u8fd9\u80fd\u529b\u4e5f\u63d0\u62d4\uff1f", "persona": "xiao_s"},
            {"text": "\u4e16\u4e8b\u96be\u6599\uff0c\u4f46\u6ca1\u5173\u7cfb\uff0c\u8fc7\u597d\u81ea\u5df1\u7684", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=11, scene="coffee",
        question="\u540c\u4e8b\u8bf4\u8981\u8bf7\u4f60\u559d\u5496\u5561\uff0c\u7ed3\u679cAA\u5236",
        options=[
            {"text": "\u6ca1\u4e8b\uff0c\u5927\u5bb6\u90fd\u4e00\u6837\u7684", "persona": "sha_seng"},
            {"text": "\u4f60\u8bf4\u8bf7\u5ba2\u7ed3\u679cAA\uff1f", "persona": "hanzawa_naoki"},
            {"text": "\u54e6\uff0c\u90a3\u6211\u4e0b\u6b21\u8bf7\u56de\u6765", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u4f60\u8fd9\u8bf7\u5ba2\u8bf7\u5f97\u633a\u7279\u522b\u554a", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u8fd9\u662f\u8bf7\u5ba2\u8fd8\u662f\u62a2\u52ab\uff1f", "persona": "xiao_s"},
            {"text": "\u5496\u5561\u7684\u94b1\u4e0d\u91cd\u8981\uff0c\u91cd\u8981\u7684\u662f\u5fc3\u60c5", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=12, scene="birthday",
        question="\u540c\u4e8b\u8fc7\u751f\u65e5\uff0c\u5728\u7fa4\u91cc\u53d1\u7ea2\u5305\uff0c\u4f60\u62a2\u5230\u4e86 0.01 \u5143",
        options=[
            {"text": "\u8c22\u8c22\uff01\u751f\u65e5\u5feb\u4e50\uff01", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e2a\u7ea2\u5305\u6709\u70b9\u5c0f\u5427", "persona": "hanzawa_naoki"},
            {"text": "\u8fd0\u6c14\u4e0d\u9519\uff0c\u62a2\u5230\u5c31\u662f\u8d5a\u5230", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u8fd9\u4e2a\u6570\u5b57\u771f\u5409\u5229\uff01", "persona": "yue_yunpeng"},
            {"text": "\u8fd9\u4e48\u5c0f\u6c14\u8fd8\u53d1\u4ec0\u4e48\u7ea2\u5305", "persona": "xiao_s"},
            {"text": "\u4e00\u5206\u94b1\u4e5f\u662f\u7231\uff0c\u6bd4\u6ca1\u6709\u5f3a", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=13, scene="wifi",
        question="\u516c\u53f8WiFi\u5f88\u5361\uff0c\u8001\u677f\u8bf4\u662f\u5927\u5bb6\u6d41\u91cf\u7528\u5f97\u592a\u591a",
        options=[
            {"text": "\u90a3\u6211\u5c11\u7528\u70b9\u624b\u673a", "persona": "sha_seng"},
            {"text": "\u8fd9\u662f\u57fa\u7840\u8bbe\u65bd\u95ee\u9898\uff0c\u4e0d\u662f\u6211\u4eec\u7684\u9519", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u770b\u770b\u80fd\u4e0d\u80fd\u7528\u81ea\u5df1\u6d41\u91cf", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u8fd9\u662f\u8ba9\u6211\u4eec\u597d\u597d\u5de5\u4f5c\u7684\u610f\u601d", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u7684WiFi\u662f\u7528\u6765\u770b\u7684\uff0c\u4e0d\u662f\u7528\u6765\u7528\u7684\uff1f", "persona": "xiao_s"},
            {"text": "\u7f51\u7edc\u4e0d\u597d\u4e5f\u662f\u4e00\u79cd\u4fee\u884c", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=14, scene="toilet",
        question="\u4e0a\u5395\u6240\u9047\u5230\u8001\u677f\uff0c\u8001\u677f\u8bf4\u4f60\u600e\u4e48\u53c8\u6765\u4e86",
        options=[
            {"text": "\u54c8\u54c8\uff0c\u6700\u8fd1\u80a0\u80c3\u4e0d\u592a\u597d", "persona": "sha_seng"},
            {"text": "\u8fd9\u662f\u6211\u7684\u4e2a\u4eba\u65f6\u95f4", "persona": "hanzawa_naoki"},
            {"text": "\u8001\u677f\u60a8\u4e5f\u6765\u4e86\uff0c\u771f\u5de7", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u6211\u4eec\u771f\u662f\u9ed8\u5951\u5341\u8db3\uff01", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u7ba1\u5f97\u6709\u70b9\u591a\u5427", "persona": "xiao_s"},
            {"text": "\u4eba\u751f\u5728\u4e16\uff0c\u6709\u6765\u6709\u5f80\uff0c\u6b63\u5e38", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=15, scene="meeting_room",
        question="\u4f60\u9884\u7ea6\u7684\u4f1a\u8bae\u5ba4\u88ab\u8001\u677f\u5360\u7528\u4e86",
        options=[
            {"text": "\u6ca1\u4e8b\uff0c\u6211\u627e\u522b\u7684\u5730\u65b9", "persona": "sha_seng"},
            {"text": "\u8fd9\u662f\u6211\u9884\u7ea6\u7684\uff0c\u60a8\u5e94\u8be5\u63d0\u524d\u8bf4", "persona": "hanzawa_naoki"},
            {"text": "\u8001\u677f\u60a8\u5148\u7528\uff0c\u6211\u7b49\u60a8", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u8001\u677f\u60a8\u8fd9\u662f\u7ed9\u6211\u653e\u5047\u5417", "persona": "yue_yunpeng"},
            {"text": "\u9884\u7ea6\u7cfb\u7edf\u662f\u6446\u8bbe\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u4f1a\u8bae\u5ba4\u4e0d\u91cd\u8981\uff0c\u91cd\u8981\u7684\u662f\u5fc3\u6001", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=16, scene="rain",
        question="\u4e0b\u96e8\u5929\u4e0b\u73ed\uff0c\u540c\u4e8b\u5f00\u8f66\u987a\u8def\u4f46\u6ca1\u95ee\u4f60\u8981\u4e0d\u8981\u642d\u8f66",
        options=[
            {"text": "\u6ca1\u4e8b\uff0c\u6211\u6253\u8f66\u56de\u53bb", "persona": "sha_seng"},
            {"text": "\u4f60\u987a\u8def\u4e0d\u987a\u6211\u5417\uff1f", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u770b\u770b\u516c\u4ea4\u600e\u4e48\u8d70", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u4f60\u8fd9\u8f66\u662f\u4e24\u5ea7\u7684\u5427", "persona": "yue_yunpeng"},
            {"text": "\u6211\u662f\u900f\u660e\u4eba\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u6dcb\u96e8\u4e5f\u662f\u4e00\u79cd\u4f53\u9a8c", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=17, scene="printer",
        question="\u6253\u5370\u673a\u5361\u7eb8\u4e86\uff0c\u540c\u4e8b\u8bf4\u662f\u4f60\u521a\u624d\u7528\u7684\u90a3\u4e2a\u4eba\u641e\u574f\u7684",
        options=[
            {"text": "\u90a3\u6211\u53bb\u770b\u770b\u80fd\u4e0d\u80fd\u4fee", "persona": "sha_seng"},
            {"text": "\u521a\u624d\u7528\u7684\u4eba\u5f88\u591a\uff0c\u4e0d\u80fd\u602a\u6211", "persona": "hanzawa_naoki"},
            {"text": "\u53ef\u80fd\u662f\u7eb8\u5f20\u95ee\u9898\uff0c\u6211\u6362\u4e00\u5305\u8bd5\u8bd5", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u6253\u5370\u673a\u4e5f\u6709\u813e\u6c14\u4e86", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u770b\u5230\u662f\u6211\u641e\u7684\uff1f", "persona": "xiao_s"},
            {"text": "\u6253\u5370\u673a\u4e5f\u9700\u8981\u4f11\u606f\uff0c\u7406\u89e3", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=18, scene="dress",
        question="\u8001\u677f\u8bf4\u4f60\u7a7f\u5f97\u4e0d\u591f\u804c\u4e1a",
        options=[
            {"text": "\u597d\u7684\uff0c\u6211\u660e\u5929\u6362\u4e00\u5957", "persona": "sha_seng"},
            {"text": "\u6211\u7684\u7a7f\u7740\u5e76\u6ca1\u6709\u5f71\u54cd\u5de5\u4f5c", "persona": "hanzawa_naoki"},
            {"text": "\u8bf7\u95ee\u60a8\u5bf9\u804c\u4e1a\u88c5\u6709\u4ec0\u4e48\u5177\u4f53\u8981\u6c42", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u6211\u8fd9\u662f\u6f6e\u6d41\u804c\u4e1a\u88c5", "persona": "yue_yunpeng"},
            {"text": "\u60a8\u662f\u65f6\u5c1a\u6742\u5fd7\u7f16\u8f91\u5417\uff1f", "persona": "xiao_s"},
            {"text": "\u8863\u670d\u53ea\u662f\u5916\u8868\uff0c\u91cd\u8981\u7684\u662f\u5185\u5fc3", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=19, scene="salary",
        question="\u53d1\u5de5\u8d44\u4e86\uff0c\u4f60\u53d1\u73b0\u7f34\u7eb3\u7684\u4e94\u9669\u4e00\u91d1\u6bd4\u5408\u540c\u4e0a\u5199\u7684\u9ad8",
        options=[
            {"text": "\u53ef\u80fd\u662f\u653f\u7b56\u8c03\u6574\u4e86\uff0c\u6ca1\u4e8b", "persona": "sha_seng"},
            {"text": "\u8fd9\u4e2a\u9700\u8981\u7ed9\u6211\u4e00\u4e2a\u89e3\u91ca", "persona": "hanzawa_naoki"},
            {"text": "\u6211\u53bb\u4eba\u4e8b\u90e8\u95e8\u95ee\u95ee\u60c5\u51b5", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u8fd9\u662f\u7ed9\u6211\u4eec\u7684\u60ca\u559c\u5417", "persona": "yue_yunpeng"},
            {"text": "\u4f60\u4eec\u8fd9\u662f\u660e\u62a2\u554a", "persona": "xiao_s"},
            {"text": "\u94b1\u8d5a\u591a\u5c11\u4e0d\u91cd\u8981\uff0c\u91cd\u8981\u7684\u662f\u5fc3\u6001", "persona": "yu_hua"},
        ]
    ),
    QuizQuestion(
        id=20, scene="resign",
        question="\u4f60\u51b3\u5b9a\u79bb\u804c\uff0c\u8001\u677f\u8bf4\u7ed9\u4f60\u52a0\u85aa\u8ba9\u4f60\u7559\u4e0b",
        options=[
            {"text": "\u90a3\u6211\u518d\u8003\u8651\u8003\u8651", "persona": "sha_seng"},
            {"text": "\u65e2\u7136\u8981\u52a0\u85aa\uff0c\u4e3a\u4ec0\u4e48\u4e0d\u65e9\u52a0", "persona": "hanzawa_naoki"},
            {"text": "\u611f\u8c22\u60a8\u7684\u8ba4\u53ef\uff0c\u6211\u9700\u8981\u65f6\u95f4\u60f3\u60f3", "persona": "zhen_huan"},
            {"text": "\u54c8\u54c8\uff0c\u65e9\u77e5\u4eca\u65e5\uff0c\u4f55\u5fc5\u5f53\u521d", "persona": "yue_yunpeng"},
            {"text": "\u73b0\u5728\u52a0\u85aa\uff1f\u65e9\u5e72\u4ec0\u4e48\u53bb\u4e86", "persona": "xiao_s"},
            {"text": "\u4eba\u751f\u5c31\u662f\u4e0d\u65ad\u7684\u9009\u62e9\uff0c\u7559\u4e0b\u4e5f\u597d\uff0c\u8d70\u4e5f\u7f62", "persona": "yu_hua"},
        ]
    ),
]


def get_question(question_id: int):
    if 1 <= question_id <= len(QUIZ_QUESTIONS):
        return QUIZ_QUESTIONS[question_id - 1]
    return None


def calculate_persona_scores(answers: list) -> dict:
    scores = {p: 0 for p in PersonaType}
    for i, answer in enumerate(answers):
        if i >= len(QUIZ_QUESTIONS):
            break
        question = QUIZ_QUESTIONS[i]
        idx = ord(answer) - ord('A')
        if 0 <= idx < len(question.options):
            persona_str = question.options[idx].get("persona", "")
            if persona_str:
                try:
                    persona = PersonaType(persona_str)
                    scores[persona] += 1
                except ValueError:
                    pass
    return scores


def get_dominant_persona(scores: dict) -> PersonaType:
    if not scores:
        return PersonaType.SHA_SENG
    max_score = max(scores.values())
    dominant = [p for p, s in scores.items() if s == max_score]
    priority = [
        PersonaType.HANZAWA_NAOKI, PersonaType.ZHEN_HUAN,
        PersonaType.YU_HUA, PersonaType.YUE_YUNPENG,
        PersonaType.XIAO_S, PersonaType.SHA_SENG,
    ]
    for p in priority:
        if p in dominant:
            return p
    return dominant[0]
