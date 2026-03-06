# 鏋舵瀯 / 鍛藉悕 / DDD 璇勫锛堢粷涓嶅欢姣曪級

> 缁撹鍏堣锛氶」鐩凡缁忓叿澶団€滄寜涓氬姟涓婁笅鏂囷紙bounded context锛夋媶鍒嗏€濈殑闆忓舰锛宍combat` 鐨?DDD 鍒嗗眰鏈€鎺ヨ繎鐩爣锛涗絾鍏ュ彛涓庘€淐ontext/State鈥濅袱濂楁鏋跺苟瀛橈紝瀵艰嚧鍛藉悕涓庡垎灞傝竟鐣屽嚭鐜扮郴缁熸€т笉涓€鑷淬€傚缓璁厛缁熶竴杩愯鏃剁姸鎬佹満涓庣敓鍛藉懆鏈熸帴鍙ｏ紝鍐嶆敹鏁?`constants/` 鐨勮亴璐ｏ紝鏈€鍚庤ˉ榻?`application` 灞備笌绔彛/閫傞厤鍣紙ports/adapters锛夈€?

## 褰撳墠浠撳簱鐨勭湡瀹炶繍琛屾灦鏋勶紙浠ヤ唬鐮佷负鍑嗭級

- 鐩墠鈥滅湡姝ｉ┍鍔ㄦ父鎴忚繍琛屸€濈殑鍏ュ彛鏄?`run_campaign.py`锛屼娇鐢?`contexts/shared/game_state_machine.py` 鐨?`GameStateMachine + BaseState`銆?
- 鏃х殑 `main.py` + `contexts/base_context.py` + `contexts/game_state_machine.py` 灞炰簬骞惰/閬楃暀瀹炵幇锛屼笌鐜版湁 `BaseState` 鐢熷懡鍛ㄦ湡骞朵笉涓€鑷达紝瀹规槗閫犳垚璇涓庣淮鎶ゆ垚鏈€?

## 鍛藉悕闂锛堥珮浼樺厛绾э級

### 1) `Context` vs `State`锛氭湳璇笉缁熶竴

- 瀹為檯杩愯锛歚MainMenuState / CampaignState / CombatState`锛坄BaseState`锛?
- 閬楃暀鍛藉悕锛歚BaseContext`銆乣Game.change_context(...)`銆乣contexts/game_state_machine.py` 鐨?`GameStateMachine`

寤鸿锛?
- 閫夊畾涓€涓湳璇綔涓衡€滃澶?瀵瑰唴閮藉敮涓€鐨勪富鏋舵瀯鍚嶈瘝鈥濓細
  - 鑻ョ户缁噰鐢?`GameStateMachine`锛氱粺涓€绉颁负 **State**锛堟帹鑽愶紝宸茬粡璺戦€氾級
  - 鍒犻櫎鎴栨樉寮忔爣璁板純鐢ㄦ棫鐨?`Context` 浣撶郴锛堟垨杩佺Щ鍒?`BaseState`锛?

### 2) `constants/` 鍛藉悕璇锛堚€滃父閲忊€濆疄闄呮壙杞戒簡閰嶇疆/鏋氫妇/UI甯冨眬/鍩熸蹇碉級

鐜扮姸锛?
- 瀛樺湪 `constants/campaign_domain.py`銆乣constants/campaign_ui.py`銆乣constants/combat_domain.py` 绛夈€?

闂锛?
- `domain` 鐩稿叧鐨勬蹇垫斁鍦ㄥ叏灞€ `constants/` 涓嬶紝浼氳鈥滈鍩熸ā鍨嬪綊灞炲摢涓?bounded context鈥濅笉娓呮櫚銆?
- `ui` 閰嶇疆涓庣帺娉?瑙勫垯甯搁噺娣锋斁锛岄毦浠ュ仛杈圭晫妫€鏌ワ紙渚嬪绂佹 domain 灞備緷璧?UI 甯搁噺锛夈€?

寤鸿锛?
- 灏?`constants/` 鎷嗗垎涓烘洿璇箟鍖栫洰褰曪紙涓嶄竴瀹氫竴姝ュ埌浣嶏級锛?
  - `config/`锛氳繍琛屾椂鍙皟鍙傦紙鍒嗚鲸鐜囥€侀煶閲忋€佸紑鍏崇瓑锛?
  - `ui_config/`锛歎I甯冨眬銆佷富棰樺紑鍏炽€佹覆鏌撳弬鏁?
  - `contexts/<ctx>/domain/constants.py`锛氳涓婁笅鏂囩殑棰嗗煙甯搁噺/瑙勫垯閿紙浠呬笟鍔″惈涔夛級
  - `contexts/<ctx>/presentation/ui_constants.py`锛氳涓婁笅鏂?UI 甯搁噺

### 3) 鐗堟湰鍚庣紑鍛藉悕锛歚player.py`

闂锛?
- 鍦?DDD/闀挎湡缁存姢閲岋紝绫诲瀷/瀹炰綋涓€鑸笉寤鸿鐢?`v2` 鍚庣紑闀挎湡瀛樺湪锛堝巻鍙插簲鐢?git 鎵胯浇锛夈€?

寤鸿锛?
- 杩囨浮鏈熷彲浠ヤ繚鐣欙紝浣嗚涓€涓€滄敼鍚嶇獥鍙ｂ€濓細绋冲畾鍚庢妸 `player.py` 鍚堝苟/閲嶅懡鍚嶄负 `player.py`銆?

## 鍒嗗眰鏄惁鍚堢悊锛燂紙涓?DDD 鐨勮创鍚堝害锛?

### 1) combat锛氬垎灞傝緝濂斤紙鎺ヨ繎 DDD + ports/adapters锛?

浼樼偣锛?
- `contexts/combat/domain/` 姣旇緝鈥滅函鈥濓紝鏈?services銆乿alues銆乪ffects銆乪nemies 绛夋槑鏄鹃鍩熷缓妯°€?
- 鏈?`infrastructure/`锛堟暟鎹牎楠屻€丏TO銆佷粨搴?鍔犺浇锛夛紝骞朵笖娴嬭瘯瑕嗙洊鐩稿澶氥€?
- 鏈?`scripts/validate_architecture.py` 璇曞浘绾︽潫 domain 杩濊鍐欏叆锛堝緢鍔犲垎锛夈€?

涓昏鏀硅繘鐐癸細
- domain 浠嶄細渚濊禆鍏ㄥ眬 `constants.*` 鍋氬紑鍏筹紙渚嬪鑳介噺褰╂睜锛夛紝寤鸿閫愭鏀逛负锛?
  - domain 鍐呴儴 `config.py`锛堝悓 context 鍐咃級
  - 鎴栭€氳繃 application 灞傛敞鍏ワ紙鏇?DDD 姝ｇ粺锛?

### 2) campaign锛氬浜庘€淪tate 浣滀负 application + presentation 鐨勫ぇ缂栨帓鍣ㄢ€?

鐜扮姸锛?
- `CampaignState` 鍚屾椂璐熻矗锛?
  - UI 浜嬩欢澶勭悊锛坧resentation锛?
  - 澶ч噺娴佺▼缂栨帓涓庢湇鍔＄粍鍚堬紙application锛?
  - 鐩存帴鎿嶄綔/鎸佹湁棰嗗煙鏁版嵁锛坉omain DTO / block 鍒楄〃锛?

浼樼偣锛?
- 宸茬粡寮€濮嬫妸閫昏緫鎶藉埌 `contexts/campaign/services/`锛坄TrackBlockService`銆乣EndTurnService` 绛夛級锛岃繖鏄線 application 灞傝蛋鐨勬纭柟鍚戙€?

椋庨櫓锛?
- `services/` 閲屽鏋滃嚭鐜板ぇ閲?`pygame_gui`銆乁I widget 鐨勫垱寤?閿€姣侊紝浼氬鑷?application/presentation 杈圭晫缁х画妯＄硦銆?

寤鸿锛?
- 鏄庣‘ `contexts/campaign/services/` 鐨勫畾浣嶏細
  - 濡傛灉瀹冧滑鏄?**application services**锛氬氨灏介噺鍙鐞嗏€滅敤渚嬬紪鎺?+ 棰嗗煙璋冪敤 + 杩斿洖 ViewModel/鍛戒护鈥?
  - UI widget 鐨勫垱寤?甯冨眬/鍛堢幇灏介噺闆嗕腑鍦?`view.py`/`ui/`锛坧resentation锛?

## 鏄惁閬靛惊 DDD锛燂紙缁撹锛?

鏁翠綋锛?*閮ㄥ垎閬靛惊**锛屽挨鍏?combat 寰堟帴杩戔€滆交閲?DDD鈥濓紱campaign 鐩墠鏇村儚鈥滀紶缁熸父鎴忕姸鎬佹満 + 鏈嶅姟鎶藉彇鈥濓紝杩樻病瀹屽叏钀藉湪 DDD 鐨勫洓灞傦紙domain/application/infrastructure/presentation锛夎竟鐣屼笂銆?

濡傛灉鐩爣鏄€滀弗鏍?DDD鈥濓紝寤鸿鐨勬紨杩涜矾绾匡細

1. **缁熶竴涓诲叆鍙ｄ笌鐢熷懡鍛ㄦ湡**锛氫互 `run_campaign.py` + `BaseState` 涓哄噯锛沗main.py` 鏄庣‘寮冪敤鎴栬縼绉汇€?
2. **鏀舵暃 constants 鐨勮亴璐?*锛氳嚦灏戝仛鍒扳€淯I 甯搁噺涓嶈 domain 渚濊禆鈥濄€佲€渄omain 甯搁噺褰掑睘鍒板悇鑷?context鈥濄€?
3. **琛ラ綈 application 灞?*锛氭妸澶嶆潅娴佺▼锛堝洖鍚堟帹杩涖€佸鍔辩粨绠椼€乵eeting 瑙﹀彂銆佹垬鏂楄矾鐢憋級闆嗕腑鎴愬彲娴嬭瘯鐨?use-cases銆?
4. **绔彛/閫傞厤鍣ㄥ寲澶栭儴渚濊禆**锛氶煶棰戙€佽祫婧愬姞杞姐€佸瓨妗ｃ€侀殢鏈烘暟绛夛紝閫氳繃鎺ュ彛闅旂锛岃 domain 鏇寸函銆佹祴璇曟洿绋炽€?

## 绔嬪埢鍙仛鐨勪笁浠跺皬浜嬶紙浣庨闄?楂樻敹鐩婏級

1. 鍦?README 鎴?docs 涓啓娓呮鈥滄寮忓叆鍙ｆ槸 `run_campaign.py`鈥濓紝骞舵爣娉?`main.py` 涓?legacy銆?
2. 缁?`scripts/validate_architecture.py` 澧炲姞瑙勫垯锛歝ombat/campaign 鐨?`domain/` 绂佹瀵煎叆 `pygame`銆乣pygame_gui`銆乣constants.*ui*`銆?
3. 绾﹀畾璺?context 渚濊禆鍙兘閫氳繃 `contexts/shared` 鎴?`shared_kernel` 鐨勭ǔ瀹氭帴鍙ｏ紙閬垮厤娣卞眰鏂囦欢浜掔浉 import锛夈€?



