# coding=utf8

class GuideConfig(object):
    INIT_GUIDE_ID = 0       # 用户注册后在用户游戏进度里初始化的引导 id
    INIT_GUIDE_STEP_ID = 0  # 用户注册后在用户游戏进度里初始化的引导步骤 id, 也是每个教程中第一步的 id
    NO_GUIDE = -1           # 当前不需要进行引导
    NO_GUIDE_STEP = -1      # 当前引导以完成
