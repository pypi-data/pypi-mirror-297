[![build status](https://img.shields.io/github/actions/workflow/status/zetxtech/embykeeper/ci.yml?branch=main)](https://github.com/zetxtech/embykeeper/commits/main) [![pypi badge](https://img.shields.io/pypi/v/embykeeper)](https://pypi.org/project/embykeeper/) [![docker](https://img.shields.io/docker/v/embykeeper/embykeeper?label=docker)](https://hub.docker.com/r/embykeeper/embykeeper) [![docker pulls](https://img.shields.io/docker/pulls/embykeeper/embykeeper?label=pulls)](https://hub.docker.com/r/embykeeper/embykeeper) [![license badge](https://img.shields.io/github/license/zetxtech/embykeeper)](https://github.com/zetxtech/embykeeper/blob/main/LICENSE) [![telegram badge](https://img.shields.io/badge/telegram-bot-blue)](https://t.me/embykeeper_bot) [![telegram badge](https://img.shields.io/badge/telegram-channel-green)](https://t.me/embykeeper) [![telegram badge](https://img.shields.io/badge/telegram-group-violet)](https://t.me/embykeeperchat)

<p align="center">
  <a href='https://github.com/zetxtech/embykeeper'>
    <img src="https://github.com/zetxtech/embykeeper/raw/main/images/logo.svg" alt="Embykeeper" />
  </a>
</p>
<p align="center">
    <b>自动签到 定时保号 按需水群</b>
</p>

---

Embykeeper 是一个用于 Emby 影视服务器的签到和保号的自动执行工具, 可以实现机器人自动签到和 Emby 服务器登陆模拟播放的功能.

## 存储库迁移

由于作者 (jackzzs) 账号莫名被封, 原 embykeeper/embykeeper 存储库已迁移到[这里](https://github.com/zetxtech/embykeeper). 之后的更新在这里进行.

## 声明

本项目涉及的一切 Emby 服务器与 Embykeeper 开发团队无关, 在使用 Embykeeper 时造成的一切损失 (包括但不限于 Emby 或 Telegram 账号被封禁或被群封禁) 与开发团队无关. 为了您的账号安全, 推荐使用小号.

本项目设计初衷是在中文 Emby 社群规则下, 保号要求逐渐苛刻 (部分要求每月登录或每日签到), 这使得休闲时间紧张的人士难以安心使用. 本项目仅旨在帮助该类人群保号, 不鼓励持有大量 Emby 账号而不使用, 导致真正需要的人、为中文影视资源分享和翻译有贡献的人难以获得账号的行为, 开发团队也呼吁仅保留 1-2 个较全面质量较高的 Emby 服务器. 本项目仅提供工具, 具体使用形式及造成的影响和后果与开发团队无关.

本项目欢迎友善讨论与建议, 您可以通过 [Github Issue](https://github.com/zetxtech/embykeeper) 途径反馈, 并认可开发团队可以关闭与项目开发不直接相关的不友善讨论. 您也可以通过 [Telegram 讨论群](https://t.me/embykeeper_chat_bot) 获得社区帮助.

Embykeeper 将自动向 "[Embykeeper Auth Bot](https://t.me/embykeeper_auth_bot)" 发送信息, 用于用户验证, 在线验证码解析, 以及日志记录, 以供定时从 "[Embykeeper Bot](https://t.me/embykeeper_bot)" 向您推送日志, 日志内容不含任何密码或密钥信息, 您认可该命令不会给您带来隐私与安全问题.

当您安装并使用该工具, 默认您已经阅读并同意上述声明, 并确认自己并非出于"集邮"目的而安装.

## 功能

- **Emby 保活**
  - 定时模拟账号登录视频播放
  - 播放时间与进度模拟
- **Telegram 机器人签到**
  - 卷毛鼠 (`jms`): [频道](https://t.me/CurlyMouse) [群组](https://t.me/Curly_Mouse) [机器人](https://t.me/jmsembybot)
  - 终点站 (`terminus`): [频道](https://t.me/embypub) [群组](https://t.me/EmbyPublic) [机器人](https://t.me/EmbyPublicBot)
  - Pornemby (`pornemby`): [频道](https://t.me/pornembyservice) [群组](https://t.me/Pornemby) [机器人](https://t.me/PronembyTGBot2_bot)
  - Apop (`apop`): [频道](https://t.me/ApopCloud_Channel) [群组](https://t.me/apopcloud) [机器人](https://t.me/apopcloudemby_bot)
  - 飞跃彩虹 (`feiyue`): [频道](https://t.me/fyemby) [群组](https://t.me/feiyueemby) [机器人](https://t.me/FeiyueEmby_bot)
  - PandaTV: [频道](https://t.me/PandaTV_Emby_Channel)
    - 自动签到 (`pandatv`): [机器人](https://t.me/PandaTV_Emby_Bot)
    - 每 14 天自动群里发送签到 (`pandatv_group`): [群组](https://t.me/PandaTV_Emby_Group)
  - 尘烬 (`skysink`): [频道](https://t.me/skysink) [机器人](https://t.me/kyououbot)
  - Peach (`peach`): [机器人](https://t.me/peach_emby_bot)
  - 魔法Emby (`magic`): [频道](https://t.me/Magic_EmbyChannel) [群组](https://t.me/Magicemby) [机器人](https://t.me/Magic_EmbyBot)
  - 开心服 (`happy`): [频道](https://t.me/hhappyemby) [群组](https://t.me/Happyembyyds) [机器人](https://t.me/hpymby_bot)
  - MICU (`micu`): [频道](http://t.me/+_PcX8rALVA80NTU1) [群组](http://t.me/+tW5vUYJROcE2ZTA1) [机器人](https://t.me/micu_user_bot)
  - 叔服Emby (`shufu`): [群组](http://t.me/+4eq37Ip8ayRhNDI9) [机器人](https://t.me/dashu660_bot)
  - 天南小筑 (`tiannan`): [频道](http://t.me/Nanflix) [群组](http://t.me/+kDBdjwtZwudhYWE1) [机器人](https://t.me/Nanflix_bot)
  - MJJ (`mjj`): [频道](https://t.me/YH_Emby) [群组](https://t.me/mjj_emby_Chat) [机器人](https://t.me/mjjemby_uesr_bot)
  - Pilipili (`pilipili`): [频道](https://t.me/PiliPiliTv) [群组](http://t.me/PiliPiliTv) [机器人](https://t.me/PiliPiliUltraTv_bot)
  - CC 公益 (`cc`): [频道](https://t.me/CcEmby) [群组](https://t.me/Embycc) [机器人](https://t.me/EmbyCc_bot)
  - 卡戎 (`charon`): [频道](https://t.me/CharonTV) [群组](https://t.me/CharonTV_Talk) [机器人](https://t.me/CharonTV_Bot)
  - Temby (`temby`): [频道](https://t.me/tembychannel) [群组](https://t.me/tembygroup) [机器人](https://t.me/HiEmbyBot)
  - 未响 (`future`): [频道](https://t.me/FutureEcho_Notice) [群组](https://t.me/FutureEcho_Chat) [机器人](https://t.me/lotayu_bot)
  - AWA 影视服 (`awatv`): [频道](https://t.me/awa_tv) [群组](https://t.me/awatv_chat) [机器人](https://t.me/awatv3_bot)
  - AWA 音乐服 (`awamusic`): [频道](https://t.me/vpsliebiao) [群组](https://t.me/vpsliebiaochat) [机器人](https://t.me/awamm_bot)
  - Lili (`lili`): [频道](https://t.me/lily_yaya) [群组](https://t.me/lilydeyaa) [机器人](https://t.me/lilyembybot)
  - 见手青 (`jsq`): [频道](https://t.me/jsq_channel) [群组](https://t.me/jsq_group) [机器人](https://t.me/jsq_ac_mg_bot)
  - DVFilm (`dvfilm`): [频道](https://t.me/dvfilmupdating) [机器人](https://t.me/DVfilm_user_bot)
  - 冰镇西瓜 (`watermelon`): [频道](https://t.me/WatermelonAirport) [群组](https://t.me/WatermelonAirportGroup) [机器人](https://t.me/XiguaEmbyBot)
  - Lyrebird (`lyrebird`): [频道](https://t.me/lyrebirdchannel) [群组](https://t.me/lyrebirdchat) [机器人](https://t.me/Lyrebird_bot)
  - 非越助手 (`sfcju`): [频道](https://t.me/sfcj_org) [群组](https://t.me/sfcj_chat) [机器人](https://t.me/sfcju_Bot)
  - Yomo (`yomo`): [频道](https://t.me/yomoemby_notice) [群组](https://t.me/yomoemby) [机器人](https://t.me/yomoemby_bot)
  - 关服, 无响应, 或已停用签到功能 (默认禁用, 请参考[Wiki](https://github.com/zetxtech/embykeeper/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6#service-%E5%AD%90%E9%A1%B9)启用):
    - Misty (`misty`): ~~[频道](https://t.me/FreeEmbyChannel) [群组](https://t.me/FreeEmby) [机器人](https://t.me/EmbyMistyBot)~~
    - Akuai (`akuai`): ~~[频道](https://t.me/Akuaitzpibgdao) [群组](https://t.me/ikuaiemby) [机器人](https://t.me/joulilibot)~~
    - 垃圾影音 (`ljyy`): ~~[群组](https://t.me/+3sP2A-fgeXg0ZmY1) [机器人](https://t.me/zckllflbot)~~
    - EmbyHub (`embyhub`): ~~[频道](https://t.me/embyhub) [群组](https://t.me/emby_hub) [机器人](https://t.me/EdHubot)~~
    - BlueSea (`bluesea`): ~~[群组](https://t.me/blueseachat) [机器人](https://t.me/blueseamusic_bot)~~
    - 卷毛鼠 IPTV (`jms_iptv`): ~~[频道](https://t.me/CurlyMouseIPTV) [群组](https://t.me/Curly_MouseIPTV) [机器人](https://t.me/JMSIPTV_bot)~~
    - Nebula (`nebula`): ~~[频道](https://t.me/Nebula_Emby) [群组](https://t.me/NebulaEmbyUser) [机器人](https://t.me/Nebula_Account_bot)~~
    - Singularity (`singularity`): ~~[频道](https://t.me/Singularity_Emby_Channel) [群组](https://t.me/Singularity_Emby_Group) [机器人](https://t.me/Singularity_Emby_Bot)~~
    - 剧狗 (`judog`): ~~[频道](https://t.me/Mulgoreemby) [机器人](https://t.me/mulgorebot)~~
    - Heisi (`heisi`): ~~[频道](https://t.me/HeisiEm) [群组](https://t.me/HeisiYi) [机器人](https://t.me/HeisiheiBot)~~
    - 阿甘正传 (`theend`): ~~[群组](https://t.me/+5vRfDeGmOKNiMzU1) [机器人](https://t.me/theendemby_bot)~~
  - 其他非 Emby 相关 (默认禁用, 请参考[Wiki](https://github.com/zetxtech/embykeeper/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6#service-%E5%AD%90%E9%A1%B9)启用):
    - AVIBI (`avibi`): [频道](https://t.me/plus_emby) [群组](https://t.me/plusemby) [机器人](https://t.me/AIVBIbot)
    - 搜书神器 (`sssq`) ([@chneez](https://github.com/zetxtech/embykeeper/pull/8) 增加): [机器人](https://t.me/sosdbot?start=fromid_6489896414)
    - 纸片 DDoS (`zhipian`): [频道](https://t.me/PaperBotnet) [机器人](https://t.me/zhipianbot?start=2zbx04e)
    - 情报局社工库 (`infsgk`) ([@GrandDuke1106](https://github.com/GrandDuke1106) 增加): [机器人](https://t.me/qbjSGKzhuquebot?start=NjQ4OTg5NjQxNA==)
    - AI 社工库 (`aisgk`): [频道](https://t.me/AISGKChannel) [机器人](https://t.me/aishegongkubot?start=AISGK_BZ5728VM)
    - 狗狗社工库 (`dogsgk`): [频道](https://t.me/DogeSGK) [机器人](https://t.me/DogeSGK_bot?start=6489896414)
    - 花花社工库 (`huasgk`): [频道](https://t.me/sgkhua) [机器人](https://t.me/sgkvipbot?start=vip_1211595)
    - 天猫社工库 (`tianmaosgk`): [机器人](https://t.me/UISGKbot?start=7s3rgxyf)
    - 平安社工库 (`pingansgk`): [机器人](https://t.me/pingansgk_bot?start=cOfqBqegLS)
    - 小熊社工库 (`bearsgk`): [机器人](https://t.me/BearSGK_bot?start=6489896414)
    - 数据社工库 (`datasgk`): [机器人](https://t.me/datasgk_bot?start=6489896414)
    - 助手社工库 (`zhushousgk`): [机器人](https://t.me/sgk001_bot?start=NjQ4OTg5NjQxNA==)
    - 星月社工库 (`starsgk`): [机器人](https://t.me/XY_SGKBOT?start=kta1ELmKuM)
    - Bit 社工库 (`bitsgk`): [机器人](https://t.me/BitSGKBot?start=a085f7b00dcf)
    - 迷你世界社工库 (`minisgk`): [机器人](https://t.me/mnsjsgkbot?start=4146989846)
    - 冰岛社工库 (`bingdaosgk`): [机器人](https://t.me/BingDaoSGKBot?start=eM81qS9k)
    - 春江社工库 (`chunjiangsgk`): [机器人](https://t.me/ChunJiang_SGK_Bot?start=J74d1R73Z)
    - Koi 社工库 ('koisgk'): [机器人](https://t.me/KoiSGKbot?start=NI5kOPo9)
    - 清风社工库 (`qingfengsgk`): [机器人](https://t.me/Weifeng007_bot?start=iTMnapPg1Y)
    - Xray 社工库 (`xraysgk`): [机器人](https://t.me/Zonesgk_bot?start=XSZAZAXSPS)
    - Seed 社工库 (`seedsgk`): [机器人](https://t.me/SeedSGKBOT?start=38weac31b)
    - Master 社工库 (`mastersgk`): [机器人](https://t.me/BaKaMasterBot?start=dWxzgkRSBj)
    - 繁花社工库 (`fanhuasgk`): [机器人](https://t.me/FanHuaSGK_bot?start=FanHua_ALCPRMHA)
    - 度娘社工库 (`baidusgk`): [机器人](https://t.me/baidusell_bot?start=6489896414)
    - 红鼻子社工库 (`rednosesgk`): [机器人](https://t.me/freesgk123_bot?start=ZZVFMECU)
    - 银联社工库 (`unionsgk`): [机器人](https://t.me/unionpaysgkbot?start=NjQ4OTg5NjQxNA==)
    - 007 社工库 (`agentsgk`): [机器人](https://t.me/sgk007_bot?start=NjQ4OTg5NjQxNA)
    - 约翰社工库 (`johnsgk`): [机器人](https://t.me/yuehanbot?start=6489896414v4fufb)
    - 知乎社工库 (`zhihusgk`): [机器人](https://t.me/zhihu_bot?start=ZHIHU_PIIIBARB)
    - Carll 社工库 1 (`carll1`): [机器人](https://t.me/Carllnet_bot?start=6489896414)
    - Carll 社工库 2 (`carll2`): [机器人](https://t.me/Carllnet2_bot?start=6489896414)
    - Ingeek 社工库 (`ingeeksgk`): [机器人](https://t.me/ingeeksgkbot?start=NjQ4OTg5NjQxNA==)
    - 叮当猫社工库 (`dingdangsgk`): [机器人](https://t.me/DingDangCats_Bot?start=d9bb127efc6127d1)
    - 魔神社工库 (`moshensgk`): [机器人](https://t.me/moshensgk_bot?start=NjQ4OTg5NjQxNA==)
    - Bost 社工库 (`bostsgk`): [机器人](https://t.me/BOST_SGK_BOT?start=6489896414)
    - Shzi (`shzi`): [机器人](https://t.me/aishuazibot?start=QvSBSqCG)
    - 飞机工具箱 (`feiji`): [机器人](https://t.me/fjtool_bot?start=6489896414C44)
    - 鸟哥轰炸 (`niaoge`): [机器人](https://t.me/nb3344bot?start=6489896414)
- **Telegram 自动监控信息**
  - Pornemby:
    - 科举考试 (`pornemby_answer`): [活动频道](https://t.me/PornembyFun)
    - 自动抢注 (`pornemby_register`): [群组](https://t.me/Pornemby)
    - 自动抢红包雨 (`pornemby_dragon_rain`): [群组](https://t.me/Pornemby)
    - 自动翻倍 (`pornemby_double`): [群组](https://t.me/Pornemby)
    - 无 HP 自动停止自动水群 (`pornemby_double`): [群组](https://t.me/Pornemby)
    - 风险时期自动停止 (`pornemby_alert`): [群组](https://t.me/Pornemby)
  - 不给看 抢邀请码 (`bgk`): [群组](https://t.me/Ephemeralemby) [机器人](https://t.me/UnknownEmbyBot)
  - 测试中的站点 (默认禁用, 请参考[Wiki](https://github.com/zetxtech/embykeeper/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6#service-%E5%AD%90%E9%A1%B9)启用):
    - 未响 抢邀请码 (`future`): [频道](https://t.me/FutureEcho_Notice) [群组](https://t.me/FutureEcho_Chat) [机器人](https://t.me/lotayu_bot)
  - 关服或无响应 (默认禁用, 请参考[Wiki](https://github.com/zetxtech/embykeeper/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6#service-%E5%AD%90%E9%A1%B9)启用):
    - 全局自动从众 (`follow`): 当在任何群组中发现 5 分钟内 5 条一样内容的消息, 会自动跟一句 (影响范围大默认禁用)
    - Misty 开注自动注册 (`misty`): ~~[频道](https://t.me/FreeEmbyChannel) [群组](https://t.me/FreeEmby) [机器人](https://t.me/EmbyMistyBot)~~
    - Polo 抢邀请码 (`polo`): ~~[频道](https://t.me/poloembyc) [群组](https://t.me/poloemby) [机器人](https://t.me/polo_emby_bot)~~
    - 剧狗 开注自动注册 (`judog`): ~~[频道](https://t.me/Mulgoreemby) [机器人](https://t.me/mulgorebot)~~
    - Embyhub 开注自动注册 (`embyhub`): ~~[频道](https://t.me/embyhub) [群组](https://t.me/emby_hub) [机器人](https://t.me/EdHubot)~~
    - Viper 抢邀请码 (`viper`): ~~[频道](https://t.me/viper_emby_channel) [群组](https://t.me/Viper_Emby_Chat) [机器人](https://t.me/viper_emby_bot)~~
- **Telegram 自动水群** (默认使用内建话术列表, 易被辨别和封禁, 请谨慎使用)
  - Pornemby (`pornemby`): [频道](https://t.me/pornembyservice) [群组](https://t.me/Pornemby) [机器人](https://t.me/PronembyTGBot2_bot) [内建话术列表](https://github.com/zetxtech/embykeeper-data/blob/main/data/pornemby-common-wl%40v1.yaml)
  - 关服或无响应 (默认禁用, 请参考[Wiki](https://github.com/zetxtech/embykeeper/wiki/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6#service-%E5%AD%90%E9%A1%B9)启用):
    - NakoNako 自动水群 (`nakonako`): ~~[群组](https://t.me/NakoNetwork) [机器人](https://t.me/nakonetwork_bot)~~

**注意**: 部分功能由于涉及竞争条件 / 付费验证码解析服务等，部分功能需要[高级用户](https://github.com/zetxtech/embykeeper/wiki/%E5%8A%9F%E8%83%BD%E8%AF%B4%E6%98%8E-%E2%80%90-%E9%AB%98%E7%BA%A7%E7%94%A8%E6%88%B7) (永久可用).

## 安装与使用

Embykeeper 支持 Docker 或 PyPI 安装 (Linux / Windows), 也支持云部署, 请点击下方按钮开始安装:

[![Setup Tutorial](https://github.com/zetxtech/embykeeper/raw/main/images/setup-button.svg)](https://github.com/zetxtech/embykeeper/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)

若您没有服务器, 您可以通过免费托管平台进行部署, 点击下方按钮开始部署:

[![Deploy to Huggingface Space](https://github.com/zetxtech/embykeeper/raw/main/images/deploy-to-hf.svg)](https://huggingface.co/spaces/embykeeper/embykeeper?duplicate=true)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Tutorial](https://github.com/zetxtech/embykeeper/raw/main/images/hf-tutorial.svg)](https://blog.zetx.tech/2024/05/19/embykeeper-hf-tutorial/)

[![Deploy to Render](https://github.com/zetxtech/embykeeper/raw/main/images/deploy-to-render.svg)](https://render.com/deploy?repo=https://github.com/zetxtech/embykeeper/tree/stable)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Tutorial](https://github.com/zetxtech/embykeeper/raw/main/images/render-tutorial.svg)](https://blog.zetx.tech/2023/06/26/embykeeper-render-tutorial)

若您有服务器, 我们推荐使用 [Docker 部署](https://github.com/zetxtech/embykeeper/wiki/Linux-Docker-%E9%83%A8%E7%BD%B2):

```bash
docker run -v $(pwd)/embykeeper:/app --rm -it --net=host embykeeper/embykeeper
```

您也可以使用 [Docker Compose 部署](https://github.com/zetxtech/embykeeper/wiki/Linux-Docker-Compose-%E9%83%A8%E7%BD%B2).

除此之外, 您还可以通过 [PyPI 安装](https://github.com/zetxtech/embykeeper/wiki/Linux-%E4%BB%8E-PyPI-%E5%AE%89%E8%A3%85) 或 [源码构建](https://github.com/zetxtech/embykeeper/wiki/Linux-%E4%BB%8E%E6%BA%90%E7%A0%81%E6%9E%84%E5%BB%BA).

更多安装和配置方面的帮助请参考 [Wiki](https://github.com/zetxtech/embykeeper/wiki).

**注意**: 请尽可能使用小号运行本工具, 运行该工具的 Telegram 账号若通过接码注册, 请使用一段时间再接入本工具.

## 运行截图

![Screenshot](https://github.com/zetxtech/embykeeper/raw/main/images/screenshot.png)

## 支持 Embykeeper

##### 开发者团队

- ~~[jackzzs](https://github.com/jackzzs)~~
- [zetxtech](https://github.com/zetxtech)

##### 通过[爱发电](https://afdian.com/a/jackzzs)赞助

![Kitty](https://github.com/zetxtech/embykeeper/raw/main/images/kitty.gif)
