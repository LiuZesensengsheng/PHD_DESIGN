# 鏋舵瀯 / 鍛藉悕 / DDD 璇勫堢粷涓嶅欢姣曪級

> 缁撹鍏堣氶」鐩凡缁忓叿澶団€滄寜涓氬姟涓婁笅鏂囷紙bounded context夋媶鍒嗏€濈殑闆忓舰宍combat` 鐨->DDD 鍒嗗眰€鎺ヨ繎鐩爣涗絾鍏ュ彛涓庘€淐ontext/State濅袱濂楁鏋跺苟瀛橈紝瀵艰嚧鍛藉悕涓庡垎灞傝竟鐣屽嚭鐜扮郴缁熸€т笉涓€鑷淬€傚缓璁厛缁熶竴杩愯鏃剁姸鎬佹満涓庣敓鍛藉懆熸帴鍙ｏ紝鍐嶆敹->`constants/` 鐨勮亴璐ｏ紝€鍚庤ˉ榻->`application` 灞備笌绔彛/閫傞厤鍣紙ports/adapters夈€->

## 褰撳墠浠撳簱鐨勭湡瀹炶繍琛屾灦鏋勶紙浠ヤ唬鐮佷负鍑嗭級

- 鐩墠滅湡姝ｉ┍ㄦ父忚繍琛屸€濈殑鍏ュ彛鏄->`run_campaign.py`屼娇鐢->`contexts/shared/game_state_machine.py` 鐨->`GameStateMachine + BaseState`->
- 鏃х殑 `main.py` + `contexts/base_context.py` + `contexts/game_state_machine.py` 灞炰簬骞惰/閬楃暀瀹炵幇屼笌鐜版湁 `BaseState` 鐢熷懡鍛ㄦ湡骞朵笉涓€鑷达紝瀹规槗閫犳垚璇涓庣淮鎶ゆ垚€->

## 鍛藉悕闂堥珮浼樺厛绾э級

### 1) `Context` vs `State`氭湳璇笉缁熶竴

- 瀹為檯杩愯歚MainMenuState / CampaignState / CombatState`坄BaseState`->
- 閬楃暀鍛藉悕歚BaseContext`乣Game.change_context(...)`乣contexts/game_state_machine.py` 鐨->`GameStateMachine`

寤鸿->
- 閫夊畾涓€涓湳璇綔涓衡€滃澶->瀵瑰唴閮藉敮涓€鐨勪富鏋舵瀯鍚嶈瘝濓細
  - 鑻ョ户缁噰鐢->`GameStateMachine`氱粺涓€绉颁负 **State**堟帹鑽愶紝宸茬粡璺戦€氾級
  - 鍒犻櫎栨樉寮忔爣璁板純鐢ㄦ棫鐨->`Context` 浣撶郴堟垨杩佺Щ鍒->`BaseState`->

### 2) `constants/` 鍛藉悕璇堚€滃父閲忊€濆疄闄呮壙杞戒簡閰嶇疆/鏋氫妇/UI甯冨眬/鍩熸蹇碉級

鐜扮姸->
- 瀛樺湪 `constants/campaign_domain.py`乣constants/campaign_ui.py`乣constants/combat_domain.py` 绛夈€->

闂->
- `domain` 鐩稿叧鐨勬蹇垫斁鍦ㄥ叏灞€ `constants/` 涓嬶紝浼氳滈鍩熸ā鍨嬪綊灞炲摢涓->bounded context濅笉娓呮櫚->
- `ui` 閰嶇疆涓庣帺娉->瑙勫垯甯搁噺娣锋斁岄毦浠ュ仛杈圭晫妫€鏌ワ紙渚嬪绂佹 domain 灞備緷璧->UI 甯搁噺夈€->

寤鸿->
- 灏->`constants/` 鎷嗗垎涓烘洿璇箟鍖栫洰褰曪紙涓嶄竴瀹氫竴姝ュ埌浣嶏級->
  - `config/`氳繍琛屾椂鍙皟鍙傦紙鍒嗚鲸鐜囥€侀煶閲忋€佸紑鍏崇瓑->
  - `ui_config/`歎I甯冨眬佷富棰樺紑鍏炽€佹覆鏌撳弬->
  - `contexts/<ctx>/domain/constants.py`氳涓婁笅鏂囩殑棰嗗煙甯搁噺/瑙勫垯閿紙浠呬笟″惈涔夛級
  - `contexts/<ctx>/presentation/ui_constants.py`氳涓婁笅鏂->UI 甯搁噺

### 3) 堟湰鍚庣紑鍛藉悕歚player.py`

闂->
- 鍦->DDD/闀挎湡缁存姢閲岋紝绫诲瀷/瀹炰綋涓€鑸笉寤鸿鐢->`v2` 鍚庣紑闀挎湡瀛樺湪堝巻鍙插簲鐢->git 鎵胯浇夈€->

寤鸿->
- 杩囨浮熷彲浠ヤ繚鐣欙紝浣嗚涓€涓€滄敼鍚嶇獥鍙ｂ€濓細绋冲畾鍚庢妸 `player.py` 鍚堝苟/閲嶅懡鍚嶄负 `player.py`->

## 鍒嗗眰鏄惁鍚堢悊燂紙涓->DDD 鐨勮创鍚堝害->

### 1) combat氬垎灞傝緝濂斤紙鎺ヨ繎 DDD + ports/adapters->

浼樼偣->
- `contexts/combat/domain/` 姣旇緝滅函濓紝->services乿alues乪ffects乪nemies 绛夋槑鏄鹃鍩熷缓妯°€->
- ->`infrastructure/`堟暟鎹牎楠屻€丏TO佷粨搴->犺浇夛紝骞朵笖娴嬭瘯瑕嗙洊鐩稿澶氥€->
- ->`scripts/validate_architecture.py` 璇曞浘绾︽潫 domain 杩濊鍐欏叆堝緢犲垎夈€->

涓昏鏀硅繘鐐癸細
- domain 浠嶄細渚濊禆鍏ㄥ眬 `constants.*` 鍋氬紑鍏筹紙渚嬪鑳介噺褰╂睜夛紝寤鸿閫愭鏀逛负->
  - domain 鍐呴儴 `config.py`堝悓 context 鍐咃級
  - 栭€氳繃 application 灞傛敞鍏ワ紙鏇->DDD 姝ｇ粺->

### 2) campaign氬浜庘€淪tate 浣滀负 application + presentation 鐨勫ぇ缂栨帓鍣ㄢ€->

鐜扮姸->
- `CampaignState` 鍚屾椂璐熻矗->
  - UI 浜嬩欢澶勭悊坧resentation->
  - 澶ч噺娴佺▼缂栨帓涓庢湇＄粍鍚堬紙application->
  - 鐩存帴鎿嶄綔/鎸佹湁棰嗗煙版嵁坉omain DTO / block 鍒楄〃->

浼樼偣->
- 宸茬粡寮€濮嬫妸閫昏緫鎶藉埌 `contexts/campaign/services/`坄TrackBlockService`乣EndTurnService` 绛夛級岃繖鏄線 application 灞傝蛋鐨勬纭柟鍚戙€->

椋庨櫓->
- `services/` 閲屽鏋滃嚭鐜板ぇ閲->`pygame_gui`乁I widget 鐨勫垱寤->閿€姣侊紝浼氬鑷->application/presentation 杈圭晫缁х画妯＄硦->

寤鸿->
- 鏄庣‘ `contexts/campaign/services/` 鐨勫畾浣嶏細
  - 濡傛灉瀹冧滑鏄->**application services**氬氨灏介噺鍙鐞嗏€滅敤渚嬬紪鎺->+ 棰嗗煙璋冪敤 + 杩斿洖 ViewModel/鍛戒护->
  - UI widget 鐨勫垱寤->甯冨眬/鍛堢幇灏介噺闆嗕腑鍦->`view.py`/`ui/`坧resentation->

## 鏄惁閬靛惊 DDD燂紙缁撹->

翠綋->*閮ㄥ垎閬靛惊**屽挨鍏->combat 寰堟帴杩戔€滆交閲->DDD濓紱campaign 鐩墠鏇村儚滀紶缁熸父忕姸鎬佹満 + 嶅姟鎶藉彇濓紝杩樻病瀹屽叏钀藉湪 DDD 鐨勫洓灞傦紙domain/application/infrastructure/presentation夎竟鐣屼笂->

濡傛灉鐩爣鏄€滀弗鏍->DDD濓紝寤鸿鐨勬紨杩涜矾绾匡細

1. **缁熶竴涓诲叆鍙ｄ笌鐢熷懡鍛ㄦ湡**氫互 `run_campaign.py` + `BaseState` 涓哄噯沗main.py` 鏄庣‘寮冪敤栬縼绉汇€->
2. **鏀舵暃 constants 鐨勮亴璐->*氳嚦灏戝仛鍒扳€淯I 甯搁噺涓嶈 domain 渚濊禆濄€佲€渄omain 甯搁噺褰掑睘鍒板悇鑷->context濄€->
3. **琛ラ綈 application 灞->*氭妸澶嶆潅娴佺▼堝洖鍚堟帹杩涖€佸辩粨绠椼€乵eeting 瑙﹀彂佹垬鏂楄矾鐢憋級闆嗕腑愬彲娴嬭瘯鐨->use-cases->
4. **绔彛/閫傞厤鍣ㄥ寲澶栭儴渚濊禆**氶煶棰戙€佽祫婧愬姞杞姐€佸瓨妗ｃ€侀殢烘暟绛夛紝閫氳繃鎺ュ彛闅旂岃 domain 鏇寸函佹祴璇曟洿绋炽€->

## 绔嬪埢鍙仛鐨勪笁浠跺皬浜嬶紙浣庨闄->楂樻敹鐩婏級

1. 鍦->README ->docs 涓啓娓呮滄寮忓叆鍙ｆ槸 `run_campaign.py`濓紝骞舵爣娉->`main.py` 涓->legacy->
2. 缁->`scripts/validate_architecture.py` 澧炲姞瑙勫垯歝ombat/campaign 鐨->`domain/` 绂佹瀵煎叆 `pygame`乣pygame_gui`乣constants.*ui*`->
3. 绾﹀畾璺->context 渚濊禆鍙兘閫氳繃 `contexts/shared` 鐨勭ǔ瀹氭帴鍙ｏ紙閬垮厤娣卞眰鏂囦欢浜掔浉 import夈€->



