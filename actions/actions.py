from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random
import re
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk import Action


class ActionHandleAssessment(Action):
    def name(self):
        return "action_handle_assessment"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text")

        match = re.search( r"alama ya (PHQ-9|GAD-7):\s*(\d+)\s*\|\s*athari kwa maisha ya kila siku:\s*(.+)", user_message)

        if not match:
            dispatcher.utter_message(text="Samahani, siwezi kuelewa matokeo yako. Tafadhali jaribu tena.")
            return []

        test_type = match.group(1)
        score = int(match.group(2))
        impact = match.group(3).strip().lower()



        general_explanation = {
            "PHQ-9": "PHQ-9 hupima kiwango cha unyogovu. Alama za chini zinaonyesha unyogovu mdogo, na alama za juu zinaonyesha unyogovu mkubwa.",
            "GAD-7": "GAD-7 hupima kiwango cha wasiwasi. Alama za chini zinaonyesha wasiwasi mdogo, na alama za juu zinaonyesha wasiwasi mkubwa."
        }


        score_interpretation = ""
        impact_analysis = ""
        guidance = ""

        if test_type == "PHQ-9":
            if score <= 4:
                score_interpretation = "Matokeo haya yanaonyesha kuwa huna dalili za unyogovu au una dalili chache sana. Hali hii ni ya kawaida, na mara nyingi inaweza kusababishwa na changamoto za maisha ya kila siku. Unyogovu huu hauathiri maisha yako kwa kiwango kikubwa na unaweza kuendelea na shughuli zako za kila siku bila matatizo makubwa. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Dalili zako za unyogovu ni za kiwango cha chini na hazina athari yoyote kubwa kwenye maisha yako ya kila siku. Unaweza kuendelea na kazi, masomo, na shughuli zako bila changamoto kubwa."
                    guidance = " Endelea kujitunza kwa kushiriki shughuli unazozipenda, kufanya mazoezi ya mara kwa mara, kula vyema, na kulala vya kutosha. Kudumisha mawasiliano na marafiki na familia kunaweza kusaidia katika kuimarisha afya yako ya kiakili. Ikiwa utahisi mabadiliko katika hisia zako, ni vyema kuzingatia mbinu za kujituliza au kutafuta ushauri mapema."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = "Ingawa dalili zako ni ndogo, mara kwa mara unaweza kuhisi msongo wa mawazo au kutokuwa na motisha. Hali hii bado haijaathiri maisha yako kwa kiwango kikubwa, lakini inaweza kusababisha kushuka kwa ari na uchovu wa kiakili katika baadhi ya nyakati."
                    guidance = "Kujihusisha na mbinu za kupunguza msongo wa mawazo kama vile kupumua kwa kina, kufanya mazoezi ya kutuliza akili kama kutembea au yoga, na kuandika hisia zako kunaweza kusaidia. Ikiwa unahisi hali yako inazidi kuwa mbaya, fikiria kuzungumza na mtu unayemwamini ili kupata mtazamo tofauti na msaada wa kihisia."
                elif impact == "vigumu sana":
                    impact_analysis = "Hata kama dalili zako ni chache, zinaweza kuwa nzito kwako mara kwa mara na kufanya shughuli fulani kuwa changamoto. Unaweza kujikuta unakosa motisha, kuchoka kiakili, au kuwa na hisia za huzuni ambazo huja na kupita."
                    guidance = "Ni muhimu kutambua vyanzo vya hisia hizi na kutafuta njia za kukabiliana nazo kabla hazijawa mzigo mkubwa. Fanya mazoezi ya utulivu, weka ratiba thabiti ya kulala, na hakikisha unapata muda wa kupumzika. Ikiwa hali inazidi kuwa ngumu, tafuta msaada wa kitaalamu au mshauri wa karibu."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = " Ingawa dalili zako ni chache, zinaonekana kuwa na athari kubwa kwenye maisha yako ya kila siku. Hali hii inaweza kuathiri utendaji wako kazini, masomoni, au mahusiano yako na wengine, hata kama si mara kwa mara."
                    guidance = " Hii ni ishara kwamba afya yako ya kiakili inahitaji uangalizi zaidi. Tafuta njia za kujituliza, kama vile kufanya mazoezi, kushiriki shughuli za kijamii, na kuepuka upweke. Ikiwa unahisi hali yako inazidi kuwa mbaya, tafuta msaada wa kitaalamu mapema ili kuepuka changamoto kubwa baadaye"

            elif score <= 9:

                score_interpretation = "Matokeo haya yanaonyesha kuwa una dalili za unyogovu wa kiwango cha chini. Hali hii inaweza kusababisha kupungua kwa ari, uchovu wa kihisia, na hisia za huzuni mara kwa mara. "

                if impact == "sio vigumu kabisa":

                    impact_analysis = "Unyogovu wako ni wa kiwango cha chini na hauathiri maisha yako ya kila siku kwa kiwango kikubwa. Unaweza kufanya kazi zako na kushiriki shughuli za kijamii bila matatizo makubwa."

                    guidance = " Endelea kudumisha afya yako ya kiakili kwa kushiriki shughuli zinazokufurahisha, kudhibiti msongo wa mawazo, na kuwa na mawasiliano mazuri na watu wanaokutia moyo."

                elif impact == "ugumu kiasi fulani":

                    impact_analysis = "Unahisi hisia za huzuni au msongo wa mawazo mara kwa mara, na hii inaweza kuathiri motisha yako na umakini wako katika kazi au masomo."

                    guidance = " Jaribu kushiriki katika shughuli zinazokufanya uhisi vizuri, kama vile mazoezi, kusikiliza muziki, au kuzungumza na marafiki wa karibu. Ikiwa dalili hizi zinaendelea, fikiria kuwasiliana na mshauri wa afya ya akili kwa mwongozo zaidi."

                elif impact == "vigumu sana":

                    impact_analysis = " Dalili zako zinaathiri sehemu fulani za maisha yako, na unahisi uzito wa kihisia mara kwa mara. Unaweza kuwa na ugumu wa kuzingatia majukumu au kuhisi kuzidiwa na hisia zako."

                    guidance = "Ni muhimu kutafuta mbinu za kushughulikia hali hii, kama vile kufanya mazoezi ya utulivu, kusoma vitabu vya kujitambua, au kuzungumza na mtu unayemwamini. Ikiwa hali inaendelea kuwa ngumu, fikiria kutafuta msaada wa kitaalamu."

                else:  # impact == "vigumu kupita kiasi"

                    impact_analysis = "Dalili zako zinaathiri sana maisha yako ya kila siku, na unaweza kuhisi kuzidiwa na hali hii mara kwa mara. Unaweza kuwa na ugumu wa kufanya kazi zako za kila siku, kujihusisha na watu, au kupata motisha."

                    guidance = "Hii ni ishara kwamba unahitaji msaada wa haraka wa kitaalamu. Tafuta usaidizi kutoka kwa mtaalamu wa afya ya akili ili upate mwongozo bora wa kukabiliana "

            elif score <= 14:
                score_interpretation = "Matokeo haya yanaonyesha kuwa una dalili za unyogovu wa kiwango cha kati. Hali hii inaweza kuathiri hisia zako, uwezo wa kufanya kazi, na mahusiano yako na wengine. Unaweza kuhisi huzuni mara nyingi, kupoteza hamu ya kushiriki katika shughuli ulizokuwa ukifurahia, na kuwa na changamoto za umakini au usingizi. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Ingawa una dalili za unyogovu wa kiwango cha kati, bado una uwezo wa kuendelea na maisha yako ya kila siku bila matatizo makubwa. Hali hii inaweza kuwa ya muda mfupi au kusababishwa na hali fulani zinazokufanya uhisi huzuni au kupoteza ari."
                    guidance = "Ni muhimu kuzingatia afya yako ya kiakili kwa kudumisha ratiba ya kawaida, kushiriki mazoezi ya mwili, na kuzungumza na mtu unayemwamini kuhusu hisia zako. Ikiwa dalili zinaendelea kwa muda mrefu, fikiria kutafuta msaada wa kitaalamu ili kupata mwongozo wa kudhibiti hali yako."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = " Dalili zako zinaanza kuwa na athari kwenye maisha yako ya kila siku. Unaweza kujikuta unapoteza motisha, kushindwa kufurahia shughuli, au kuwa na hisia za uchovu wa kihisia mara kwa mara."
                    guidance = "Jaribu kufanya mazoezi ya kupunguza msongo wa mawazo, kama vile mindfulness, kutembea nje, au kuandika hisia zako. Pia, kuzungumza na marafiki au familia inaweza kusaidia. Ikiwa hali yako haibadiliki au inazidi kuwa mbaya, tafuta msaada kutoka kwa mtaalamu wa afya ya akili."
                elif impact == "vigumu sana":
                    impact_analysis = " Dalili zako zinaanza kuathiri maeneo muhimu ya maisha yako, kama vile kazi, mahusiano, na uwezo wa kushughulikia majukumu ya kila siku. Unaweza kuhisi kuzidiwa na hisia zako mara kwa mara."
                    guidance = "Ni muhimu kushughulikia hali hii mapema kwa kutafuta msaada wa kitaalamu. Unaweza kuzungumza na mshauri wa afya ya akili, kujaribu tiba ya utambuzi wa kitabia (CBT), au kushiriki katika vikundi vya usaidizi vya afya ya kiakili. Kujihusisha na shughuli unazozipenda na kudhibiti usingizi wako pia kunaweza kusaidia."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = " Dalili zako zinaathiri sana maisha yako, na inaweza kuwa vigumu kwako kufanya kazi, kuwasiliana na wengine, au kupata motisha ya kufanya mambo ya kila siku."
                    guidance = "Unahitaji msaada wa kitaalamu haraka. Tafuta usaidizi kutoka kwa mshauri wa afya ya akili au daktari. Unaweza kufikiria tiba ya kitabia au hata matibabu ya dawa ikiwa yatapendekezwa na mtaalamu. Usijitenge—tafuta msaada kutoka kwa familia, marafiki, au mtu unayemwamini."
            # Score ≥ 15
            else:
                score_interpretation = "Matokeo haya yanaonyesha kuwa una unyogovu wa kiwango cha juu , ambao una athari kubwa kwa maisha yako ya kila siku. Dalili kama huzuni sugu, kupoteza hamu ya maisha, matatizo ya usingizi, na uchovu wa kihisia vinaweza kuwa vya kawaida kwako.  "
                if impact == "sio vigumu kabisa":
                    impact_analysis = ": Ingawa una dalili kali za unyogovu, bado unajitahidi kuendelea na maisha yako ya kila siku. Hata hivyo, hali hii inaweza kuendelea kuzorota ikiwa haitashughulikiwa."
                    guidance = " Unapaswa kuchukua hatua sasa. Tafuta mbinu za kujituliza kama mazoezi, mindfulness, au kuzungumza na mtu unayemwamini. Ikiwa dalili hizi zinaendelea, tafuta msaada wa kitaalamu haraka."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = "Unyogovu wako unaanza kuathiri kazi, mahusiano, na furaha yako ya maisha. Unaweza kuhisi huzuni, uchovu wa kihisia, au kupoteza motisha mara kwa mara."
                    guidance = "Tafuta msaada kutoka kwa mshauri wa afya ya akili. Kuanzisha mazoezi ya utulivu kama yoga au kuandika hisia zako kunaweza kusaidia. Ikiwa hali inazidi kuwa mbaya, usisite kuwasiliana na daktari."
                elif impact == "vigumu sana":
                    impact_analysis = " Dalili zako zinaingilia sehemu muhimu za maisha yako, na inaweza kuwa vigumu kwako kushughulikia majukumu yako ya kila siku."
                    guidance = "Tafuta msaada wa kitaalamu mara moja. Unyogovu wa kiwango hiki unahitaji tiba ya kitabia na huenda hata matibabu ya dawa. Usiendelee kujitenga—tafuta msaada kutoka kwa wapendwa wako."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = " Unyogovu wako unaathiri sana maisha yako, na huenda unahisi huna udhibiti wa hali yako."
                    guidance = " Msaada wa haraka wa kitaalamu unahitajika. Tafuta mshauri wa afya ya akili au daktari kwa matibabu yanayofaa. Ikiwa hali inakuwa mbaya zaidi, wasiliana na huduma za dharura za afya ya akili."
        elif test_type == "GAD-7":
            if score <= 4:
                score_interpretation = " Matokeo haya yanaonyesha una wasiwasi mdogo. Hii inamaanisha kuwa una wasiwasi chini ambao ni wa kawaida na unaoweza kutokea katika maisha ya kila siku, kama vile kufikiria majukumu ya kazi, masomo, au mahusiano. Wasiwasi huu hauna athari kubwa kwa ustawi wako, na mara nyingi huja na kupita bila kuathiri maisha yako kwa kiasi kikubwa. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Hali ya wasiwasi ni ndogo na haiathiri maisha yako. Unaweza kuendelea na kazi zako bila matatizo yoyote, na huna dalili zinazoingilia ustawi wako wa kila siku."
                    guidance = "Endelea kudumisha hali nzuri ya afya ya akili kwa kushiriki shughuli unazozipenda, kupata muda wa kupumzika, na kuwa na mtazamo mzuri wa maisha. Ikiwa utahitaji msaada wakati wowote, usisite kuwasiliana na wapendwa wako au mtaalamu wa afya ya akili. Kila mtu hukumbana na msongo wa mawazo mara kwa mara, na ni muhimu kujali afya yako ya akili."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = " Wasiwasi wako ni wa kiwango cha chini, lakini unahisi msongo wa mawazo mara kwa mara. Unaweza kuwa na hisia za wasiwasi unapokutana na changamoto fulani, lakini bado una uwezo wa kuzishughulikia."
                    guidance = "Kupambana na hali hii, fanya mazoezi ya kudhibiti mawazo, kama vile kupumua kwa kina na kuandika hisia zako. Kupunguza muda wa kutumia mitandao ya kijamii na kujihusisha na watu wanaokutia moyo kunaweza kusaidia pia. Ikiwa unahisi wasiwasi wako unaongezeka, usisite kuzungumza na mtu unayemwamini au kutafuta ushauri kutoka kwa mtaalamu."
                elif impact == "vigumu sana":
                    impact_analysis = "Wasiwasi mdogo unaanza kuathiri maisha yako, hata kama si kwa kiwango kikubwa. Hii inamaanisha kuwa ingawa dalili zako si za mara kwa mara, zinapotokea, zinaweza kuwa nzito sana kwako."
                    guidance = "Ni muhimu kuelewa ni hali zipi zinakufanya ujihisi hivi na kutafuta njia bora za kukabiliana nazo, kama  kufanya mazoezi ya kupunguza msongo wa mawazo, au kuzungumza na mtu unayemwamini. Pia unaweza kuzungumza na mtaalamu wa afya ya akili, kwani anaweza kukupa mbinu zinazokusaidia kudhibiti wasiwasi kwa ufanisi. Kuchukua hatua ndogo sasa kunaweza kusaidia kuzuia changamoto kubwa baadaye."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = "Wasiwasi wako, hata kama ni mdogo, unaathiri sana maisha yako ya kila siku, kama uwezo wako wa kufanya kazi, kupumzika, kufurahia maisha na mengine mengi. Unaweza kuhisi hofu au mfadhaiko mkubwa kwa sababu ya mawazo yasiyodhibitika."
                    guidance = "Ni muhimu kuweka afya yako ya akili mbele na kutafuta mbinu zinazokusaidia kuhisi kuwa na udhibiti zaidi wa hali yako. Kutafuta msaada kutoka kwa mtaalamu kunaweza kusaidia kuelewa kwa nini wasiwasi unakuathiri kwa njia hii na hatua unazoweza kuchukua ili kuudhibiti vyema. Kumbuka, hauko peke yako, na msaada upo kwa ajili yako."

            elif score <= 9:

                score_interpretation = "Alama hii inaonesha kuwa una wasiwasi wastani. Hii inamaanisha kuwa mara kwa mara unahisi msongo wa mawazo au hofu, lakini bado unaweza kudhibiti hali hii kwa kiasi fulani. Wasiwasi huu unaweza kuathiri baadhi ya nyanja za maisha yako, kama vile uwezo wa kuzingatia kazi, kushiriki katika shughuli za kijamii, au kulala vizuri. "

                if impact == "sio vigumu kabisa":

                    impact_analysis = "Unapata hisia za wasiwasi mara kwa mara, lakini hazileti madhara katika maisha yako. Wasiwasi huu haukufanyi ushindwe kufanya mambo yako ya kila siku. Unaweza kuwa na mawazo yanayojirudia kuhusu kazi, masomo, au maisha kwa ujumla, lakini bado unaweza kuyashughulikia bila kuhisi kuzidiwa."

                    guidance = " Endelea kutumia mbinu za kudhibiti wasiwasi kama vile kufanya mazoezi ya kupumua kwa kina, kuandika mawazo yako kwenye daftari, na kushiriki mazungumzo ya kirafiki na watu wanaokuunga mkono. Pia, hakikisha unapata muda wa kupumzika ili akili yako ipate nafasi ya kutulia. Ikiwa utagundua kuwa wasiwasi wako unaongezeka, kutafuta msaada mapema kunaweza kusaidia kuzuia changamoto zaidi"

                elif impact == "ugumu kiasi fulani":

                    impact_analysis = "Wasiwasi wako unakufanya uhisi msongo wa mawazo mara kwa mara, na umeanza kusababisha changamoto kidogo katika maisha yako ya kila siku. Ingawa bado unaweza kudhibiti hali hii, unahitaji juhudi za ziada kudumisha ustawi wako wa kiakili."

                    guidance = "Shughuli kama mazoezi, kupanga ratiba ya kazi zako vizuri, au kuzungumza na rafiki zinaweza kukusaidia kuhisi utulivu zaidi wa hali yako. Ikiwa changamoto hizi zitaendelea, kutafuta ushauri wa kitaalamu kunaweza kuwa hatua nzuri ya kuchukua."

                elif impact == "vigumu sana":

                    impact_analysis = "Wasiwasi wako unaanza kuathiri kwa kiasi kikubwa jinsi unavyohisi na unavyofanya kazi zako. Unaweza kuhisi uchovu wa kiakili na kimwili mara kwa mara, ukipata ugumu wa kuzingatia au kushughulikia majukumu yako ipasavyo, na pia kuwa na hofu isiyoeleweka."

                    guidance = " Ni muhimu kuzingatia mbinu za kudhibiti hali yako. Tafuta muda wa kufanya shughuli zinazokuletea furaha, kama vile kusikiliza muziki wa utulivu au kusoma vitabu vya kuhamasisha. Jaribu pia kufanya mazoezi na kupumua kwa kina mara kwa mara. Ikiwa hali hii inaendelea na inaanza kukulemea zaidi, tafuta msaada kutoka kwa mshauri wa afya ya akili au mshauri wa karibu ambaye anaweza kusaidia kukupa mwongozo sahihi."

                else:  # impact == "vigumu kupita kiasi"

                    impact_analysis = "Wasiwasi wako unaanza kuathiri sana maisha yako. Kiasi hiki ni kwamba unashindwa kufanya mambo yanavyofaa kufanywa au unajikuta unakwepa shughuli fulani kwa sababu ya hofu au msongo wa mawazo. Hali hii inafanya unahisi kuzidiwa na hofu, hata kwa mambo madogo ambayo hapo awali hayakuwa na uzito mkubwa kwako."

                    guidance = "Hii ni ishara kwamba unahitaji msaada wa ziada wa kitaalamu. Usisite kuzungumza na mshauri wa afya ya akili ili kupata mwongozo wa kudhibiti hali hii. Unaweza pia kujaribu njia za kupunguza msongo wa mawazo, kama vile kufanya mazoezi ya utulivu, kufanya mazoezi ya kupumua, kuzungumza na mtu unayemwamini, na kuhakikisha unapata usingizi wa kutosha."

            elif score <= 14:
                score_interpretation = "Matokeo haya yanaonyesha una wasiwasi wa kati. Hii inamaanisha kuwa wasiwasi wako ni wa mara kwa mara na unaweza kuathiri maisha yako ya kila siku kwa kiasi kikubwa. Unaweza kupata ugumu wa kuzingatia kazi au masomo, kuhisi kuchoka kihisia na kimwili, au hata kuepuka shughuli fulani kwa sababu ya hofu au msongo wa mawazo. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Ingawa una kiwango cha kati cha wasiwasi, unaweza kuendelea na shughuli zako za kila siku bila kupata changamoto kubwa. Hata hivyo, bado unaweza kuhisi msongo wa mawazo unaojitokeza mara kwa mara, hasa katika mazingira yenye shinikizo kubwa. Unaweza pia kuwa na mawazo mengi yanayojirudia, lakini bado unaweza kuyadhibiti kwa kiasi fulani."
                    guidance = " Endelea kufuatilia hali yako ya kihisia na kuhakikisha kuwa wasiwasi huu hauongezeki. Jaribu kufanya shughuli zinazokufanya uhisi vizuri, kama vile kutembea, kusikiliza muziki wa utulivu, au kutumia muda na marafiki wa karibu. Pia, epuka tabia zinazoweza kuchochea wasiwasi kama vile kutokuwa na ratiba nzuri au kulala kwa muda mfupi."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = " Wasiwasi wako unaanza kuwa mzito na unakulemea kwa kiasi fulani. Unaweza kuhisi ugumu wa kuzingatia, kushuka kwa kiwango cha kufanya mambo kazini au darasani, au kuwa na hisia za kukata tamaa mara kwa mara. Huenda ukahisi kama unajitahidi sana kufanya mambo ambayo hapo awali hayakuwa magumu kwako."
                    guidance = "Hali hii inaweza kushughulikiwa kutumia mbinu za kudhibiti msongo wa mawazo kama vile kuandika mawazo yako kwenye daftari au kufanya mazoezi ya kupumua kwa kina. Pia, jaribu kupanga ratiba yako kwa uangalifu ili kupunguza msongo wa mawazo unaotokana na kazi nyingi. Ikiwa hali inaendelea kuwa ngumu, usisite kutafuta ushauri kutoka kwa mtu unayemwamini au kwa mtaalamu wa afya ya akili."
                elif impact == "vigumu sana":
                    impact_analysis = "Wasiwasi wako unaathiri maisha yako kwa kiasi kikubwa. Unaweza kupoteza motisha ya kufanya mambo uliyokuwa ukifurahia. Hali ya hofu inaweza kujitokeza mara kwa mara, hata kwa mambo madogo ambayo hapo awali hayakuwa na uzito mkubwa kwako, na inaweza kukufanya uhisi kutokuwa salama au kushindwa kudhibiti hali yako."
                    guidance = "Ili kusaidia kupunguza wasiwasi, hakikisha unajitunza kwa makusudi na unajipa muda wa kupumzika. Tafuta msaada kutoka kwa marafiki wa karibu, familia, au mtaalamu wa afya ya akili ili upate usaidizi wa kihisia na kisaikolojia. Pia, shiriki katika shughuli zinazokuletea utulivu wa kiakili kama vile kufanya mazoezi, kusikiliza muziki wa kutuliza, au kusoma vitabu vya kuhamasisha. Ikiwa unahisi hali yako inaendelea kuwa ngumu, ni muhimu kutafuta msaada wa kitaalamu."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = " Wasiwasi wako umekithiri na unakulemea kwa kiwango cha juu, kiasi kwamba unapata ugumu mkubwa kushughulikia majukumu ya kila siku. Unaweza kuhisi hofu kali inayoathiri uwezo wako wa kufanya maamuzi, kushuka kwa motisha, na kupoteza kabisa uwezo wa kufurahia mambo uliyokuwa ukipenda."
                    guidance = "Hii ni ishara kwamba unahitaji msaada wa kitaalamu haraka. Tafuta mshauri wa afya ya akili ili upate njia bora za kushughulikia wasiwasi wako. Pia, jaribu kutengeneza mfumo wa msaada kwa kushirikiana na marafiki au familia ili usihisi uko peke yako katika hali hii. Ikiwa unahisi hali inazidi kuwa mbaya, usisite kutafuta msaada wa dharura kutoka kwa wataalamu wa afya."
            # Score ≥ 15
            elif score <=19:
                score_interpretation = "Alama hii inaonesha kuwa una wasiwasi mkubwa. Hii ina maana kuwa wasiwasi huu unaweza kusababisha hofu kali, msongo wa mawazo sugu, na hata dalili za kimwili kama maumivu ya kichwa, kushindwa kulala, au maumivu ya misuli. Unaweza kuhisi kama akili yako imelemewa na mawazo yanayojirudia, na hali hii inaweza kuathiri kazi, mahusiano, na afya yako kwa ujumla. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Ingawa una kiwango cha juu cha wasiwasi, bado una uwezo wa kushughulikia shughuli zako za kila siku vizuri. Hata hivyo, msongo wa mawazo huu unaweza kuwa mzito na kuchukua nguvu nyingi za kiakili na kimwili. Unaweza kuwa na mwelekeo wa kufikiria kupita kiasi na kuhisi uchovu mara kwa mara, lakini bado una uwezo wa kushughulikia majukumu yako."
                    guidance = "Kupambana na hali hii, jitahidi kuzingatia mbinu za kupunguza msongo wa mawazo, kama vile kufanya mazoezi ya utulivu na mazoezi ya kupumua kwa kina. Pia, epuka tabia zinazoweza kuzidisha hali yako kama vile kukaa peke yako kwa muda mrefu au kushughulika na kazi nyingi bila kupumzika. Ikiwa unahisi hali hii inaendelea kwa muda mrefu, ni vyema kutafuta msaada wa kitaalamu mapema."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = "Wasiwasi wako umeanza kuathiri kidogo jinsi unavyofanya kazi . Unaweza kuwa na mzunguko wa mawazo hasi unaokufanya uhisi kama huwezi kudhibiti hali yako. Dalili kama vile kushindwa kulala vizuri na kukosa hamu ya kula zinaweza kuwa za mara kwa mara."
                    guidance = "Ni muhimu kutumia mbinu kama vile, kujenga ratiba yenye utaratibu mzuri na kufanya mazoezi, ili kupunguza msongo wa mawazo. Tafuta muda wa kupumzika na ufanye shughuli zinazokufanya ujisikie vizuri, kama vile kusikiliza muziki wa utulivu, kuandika mawazo yako, au kutumia muda na wapendwa wako. Ikiwa hali inaendelea kuwa ngumu na inakulemea, tafuta msaada wa mtaalamu wa afya ya akili ili upate mwongozo wa kitaalamu."
                elif impact == "vigumu sana":
                    impact_analysis = "Wasiwasi wako umeathiri sana uwezo wako wa kudhibiti hisia na majukumu yako ya kila siku na unakufanya unahisi kama unapoteza mwelekeo polepole. Unaweza kuhisi hofu kali hata kwa hali ambazo hapo awali hazikuwa za kutisha kwako."
                    guidance = "Hali hii inahitaji hatua za haraka za kushughulikiwa. Tafuta msaada kutoka kwa familia, marafiki, au mshauri wa afya ya akili. Pia, jaribu kuanzisha tabia chanya kama vile kufanya mazoezi ya mwili, kufuata ratiba ya kulala vizuri, na kuepuka vichocheo vya msongo kama kufanya kazi kupita kiasi. Ikiwa unahisi unalemewa na hali hii, wasiliana na mtaalamu wa afya kwa msaada wa kitaalamu."
                else:  # impact == "vigumu kupita kiasi"
                    impact_analysis = "Wasiwasi wako umefikia kiwango cha juu kiasi kwamba unahisi kama huna tena mamlaka juu ya maisha yako, na kila kitu kinakushinda kabisa. Unaweza kupata hofu kubwa sana, kuhisi kushindwa kabisa kufanya kazi zako za kila siku, au hata kuwa na mawazo ya kukata tamaa. Hali hii inaweza kusababisha matatizo makubwa kiafya ikiwa haitashughulikiwa kwa haraka."
                    guidance = "Hii ni hali inayohitaji msaada wa haraka wa kitaalamu. Tafuta mshauri wa afya ya akili ili kupata mbinu bora za kukabiliana na hali hii. Ikiwa unahisi hali hii inazidi kuwa mbaya, usisite kuwasiliana na mtaalamu wa afya mara moja. Pia, zungumza na mtu unayemwamini ili kupata msaada wa kihisia. Kumbuka kuwa hauko peke yako, na msaada upo kwa ajili yako."
            else:
                score_interpretation = "Matokeo haya yanaonyesha kuwa una dalili kali za unyogovu, ambazo zinaweza kuathiri maisha yako kwa kiwango kikubwa. Hali hii inaweza kuambatana na hisia za huzuni sugu, kuchoka kupita kiasi, kupoteza hamu ya maisha, matatizo ya usingizi (kulala kupita kiasi au kukosa usingizi), na matatizo ya kuzingatia au kufanya maamuzi. Watu wenye unyogovu mkali pia wanaweza kuwa na mawazo ya kujiudhuru au kujidhuru kimwili.Hali hii ni mbaya na inahitaji msaada wa haraka wa kitaalamu. "
                if impact == "sio vigumu kabisa":
                    impact_analysis = "Ingawa una dalili kali za unyogovu, bado una uwezo wa kuendelea na maisha yako ya kila siku bila matatizo makubwa. Hata hivyo, hali hii inaweza kuwa hatari ikiwa haitashughulikiwa kwa wakati. Unaweza kuwa unajaribu kudhibiti hisia zako peke yako, lakini unyogovu mkali unahitaji msaada wa kitaalamu ili kuhakikisha hauzidi kuwa mbaya zaidi."
                    guidance = " Ni muhimu kutambua kuwa hata kama unaendelea na maisha yako kwa sasa, dalili za unyogovu zinaweza kuwa mzigo mkubwa kimwili na kiakili. Hatua unazochukua sasa zinaweza kusaidia kuzuia hali yako kuzorota zaidi. Unapaswa kuzungumza na mtaalamu wa afya ya akili ili kupokea tathmini sahihi na mwongozo wa matibabu unaofaa. Pia, jaribu kudumisha ratiba thabiti, kupata usingizi wa kutosha, na kuepuka vichocheo vya msongo wa mawazo. Ikiwa unahisi hali yako inaanza kuwa mbaya zaidi, usisite kutafuta msaada wa haraka."
                elif impact == "ugumu kiasi fulani":
                    impact_analysis = "Dalili zako za unyogovu zinaanza kuathiri maeneo mbalimbali ya maisha yako, ikiwa ni pamoja na kazi, mahusiano, na uwezo wa kushughulikia majukumu ya kila siku. Unaweza kuhisi uchovu wa kihisia mara kwa mara, kupoteza motisha, au hata kujitenga na marafiki na familia. Inaweza kuwa vigumu kupata raha au furaha katika mambo ambayo hapo awali ulikuwa ukifurahia."
                    guidance = " Unahitaji msaada wa kitaalamu ili kudhibiti dalili hizi kabla hazijazidi kuwa mbaya. Tafuta ushauri kutoka kwa mshauri wa afya ya akili au daktari, ambaye anaweza kupendekeza tiba ya utambuzi wa kitabia (CBT) au matibabu ya dawa kulingana na tathmini ya hali yako. Kujihusisha na shughuli ndogo ndogo unazoweza kudhibiti, kama vile kutembea nje, kusikiliza muziki, au kufanya mazoezi mepesi, kunaweza kusaidia kupunguza msongo wa mawazo. Usijitenge tafuta msaada kutoka kwa marafiki, familia, au vikundi vya usaidizi."
                elif impact == "vigumu sana":
                    impact_analysis = "Unyogovu wako unaathiri kwa kiwango kikubwa maisha yako ya kila siku, na unahisi mzigo mkubwa wa kihisia. Unaweza kuwa na changamoto kubwa ya kufanya kazi, kushughulikia majukumu ya nyumbani, au kudumisha mahusiano na watu wengine. Hisia zako zinaweza kuwa nzito kiasi cha kufanya kila siku ionekane kama mzigo usio na mwisho."
                    guidance = "Hali hii inahitaji msaada wa haraka wa kitaalamu. Tafuta usaidizi kutoka kwa mshauri wa afya ya akili, daktari, au huduma za usaidizi wa afya ya akili. Ikiwa unapata mawazo ya kujidhuru au unahisi huna matumaini, ni muhimu uzungumze na mtu unayemwamini mara moja.Mbali na msaada wa kitaalamu, jaribu kuanzisha mabadiliko madogo katika maisha yako. Weka ratiba ya kulala na kula vizuri, hata kama huna hamu. Punguza matumizi ya mitandao ya kijamii ikiwa yanachangia msongo wa mawazo. Kumbuka kwamba kupata msaada sio udhaifu, bali ni hatua muhimu ya kujitunza. Hali yako inaweza kubadilika kwa msaada sahihi, na unastahili kuwa na maisha yenye amani na furaha."
                else:
                    impact_analysis = "Dalili zako zinaathiri sana maisha yako, na inaweza kuwa vigumu kufanya hata shughuli za msingi kama kuamka, kula, au kuzungumza na watu. Unaweza kuhisi kuzidiwa na huzuni kali, hofu, au hisia za kutokuwa na thamani. Ikiwa unapata mawazo ya kujiudhuru au mawazo ya kukata tamaa kabisa, hii ni ishara kwamba hali yako ni hatari na inahitaji msaada wa dharura."
                    guidance = "Hii ni hali ya dharura ya afya ya akili, na unapaswa kutafuta msaada mara moja. Tafadhali wasiliana na huduma za dharura za afya ya akili, mshauri wa afya ya akili, au mtu unayemwamini. Ikiwa unahisi huwezi kushughulikia hali hii peke yako, tafuta msaada kutoka kwa marafiki, familia, au hata taasisi za usaidizi wa afya ya akili zilizo karibu nawe."
        full_response = f"{general_explanation[test_type]}\n\n{score_interpretation}\n\n{impact_analysis}\n\n{guidance}"
        dispatcher.utter_message(text=full_response)
        return []

class ActionStressAdvice(Action):
    def name(self):
        return "action_stress_advice"
    def run(self, dispatcher, tracker, domain):
        stress_issues={}
        for slot in ["cause","symptom","intensity"]:
            value = tracker.get_slot(slot)
            if value:
                stress_issues[slot]=value
        advice = {
            "cause": [
                "Kumbuka kuwa kila mtu hupitia changamoto katika maisha, hauko peke yako.",
                "Jipe muda wa kupumzika na kutuliza akili yako unapokumbwa na hali ngumu.",
                "Tafuta mtu wa kuzungumza naye ili kupunguza uzito wa mawazo yako.",
                "Ni sawa kuhisi huzuni wakati hali ngumu zinatokea, jipe ruhusa ya kuhisi.",
                "Jaribu kuchukua hatua ndogo kila siku hata kama hali inaonekana ngumu.",
                "Kumbuka kwamba hata siku mbaya zaidi huwa na mwisho wake.",
                "Jikumbushe nguvu zako na mafanikio ya awali ili kuongeza matumaini yako.",
                "Tafuta shughuli zinazokufurahisha kama njia ya kupunguza msongo wa mawazo.",
                "Usione haya kuomba msaada unapojisikia kushindwa na hali.",
                "Chukua kila siku kama fursa mpya ya kupata afueni na nguvu mpya.",
                "Hakuna lengo linalofaa zaidi kuliko kujali afya yako ya akili na mwili.",
                "Unapohisi umekwama, kumbuka kwamba hali hii pia itapita.",
                "Inachukua muda, lakini kila hatua ndogo inakupeleka mbele.",
                "Kila hatua unayochukua ni maendeleo, hata kama hailingani na vile ulivyokuwa ukitarajia.",
                "Ni sawa kukubaliana na hali yako ya sasa na kujitolea muda kwa nafsi yako.",
                "Tafadhali kumbuka kwamba kujali nafsi yako ni muhimu kuliko lolote lingine.",
                "Unapohisi kushindwa, kumbuka kwamba sio kila mapambano yanaonekana kwa wengine.",
                "Hali ngumu si ishara ya udhaifu, bali ni uthibitisho wa uwezo wako wa kuhimili.",
                "Usikate tamaa, wakati mgumu ni sehemu ya safari ya maisha.",
                "Wakati mwingine inachukua ujasiri mkubwa kusema, 'Sina nguvu leo, lakini nitapigana kesho.'",
                "Kama unahisi kupoteza matumaini, kumbuka kuwa kuna nafasi ya kujenga matumaini mapya kila siku.",
                "Unapohisi uchovu, ni ishara ya kuwa unahitaji kupumzika ili kupata nguvu mpya.",
                "Mara nyingi, wakati unavyokuwa na furaha ndogo, ndiyo unapata nguvu kubwa ya kushinda changamoto kubwa.",
                "Weka mbele yako ndoto zako, lakini jua kuwa ni sawa kupumzika wakati mwingine.",
                "Hata ukishindwa, kumbuka kuwa kujitahidi ndio kunaleta mafanikio baadaye.",
                "Pokea kila siku kama zawadi ya kujijenga tena na tena, polepole.",
                "Tafuta nafasi ya kutafakari na kupata amani ya akili, hata kama ni kwa sekunde chache.",
                "Usijali kuhusu kile ambacho huwezi kubadilisha, tumia nguvu zako kwa kile unachoweza kuboresha.",
                "Kumbuka kuwa unafaa kupumzika na kujitunza kabla ya kuendelea mbele.",
                "Hata wakati unavyohisi kupoteza njia, kumbuka kwamba unaweza kujua njia yako tena kwa haraka.",
                "Usikate tamaa kwa sababu ya changamoto za leo; kesho kuna uwezekano wa kuleta mabadiliko.",
                "Katika hali ngumu, usikate tamaa; sehemu ya mafanikio yako ni kushinda vikwazo.",
                "Kama unajiona umekata tamaa, tafadhali kumbuka kuwa kila mtu hupitia hali kama hiyo.",
                "Usijali kuwa hufanyi vizuri kila wakati, mabadiliko yanahitaji muda na uvumilivu.",
                "Ni sawa kuwa na hisia za uchovu, lakini jipe ruhusa ya kupona na kujenga nguvu mpya.",
                "Kama unajiona katika giza, kumbuka kwamba mwangaza upo mbele yako.",
                "Inachukua muda kujifunza kuwa na huruma kwako mwenyewe katika nyakati za changamoto.",
                "Usijali kuhusu hatua kubwa, hatua ndogo ni muhimu kwa mafanikio yako.",
                "Katika kila hali ngumu, kuna somo linalokuja kukufundisha na kukusaidia kukua.",
                "Kama unapojikuta ukiwa na wasiwasi, kumbuka kwamba kupumzika ni hatua muhimu ya kupona.",
                "Kumbuka kuwa kila changamoto ni fursa ya kujifunza na kukua.",
                "Mara nyingi unachohitaji ni kujua kuwa unastahili kupumzika na kujitunza.",
                "Hata wakati unahisi unapoteza mwelekeo, kumbuka kuwa unajitahidi na hilo linathaminiwa.",
                "Usiogope kuonyesha udhaifu wako kwa wengine, ni sehemu ya nguvu yako.",
                "Kila wakati unaposhindwa, kumbuka kwamba wewe ni mtu mwenye nguvu na ustahimilivu.",
                "Unapohisi kushindwa, jua kuwa unastahili muda wa kupumzika na kujenga nguvu upya.",
                "Huzuni ni sehemu ya maisha, lakini hakikisha unajitunza wakati wote.",
                "Kila wakati unapohisi umekwama, kumbuka kuwa umejijenga zaidi kuliko unavyodhani.",
                "Kumbuka kuwa kila wakati unachukua mapumziko, unajijenga kwa ajili ya hatua zako zijazo.",
                "Inachukua ujasiri mkubwa kukubaliana na hali yako na kisha kuchukua hatua kwa polepole.",
                "Hata wakati maumivu ya kihisia ni makali, kumbuka kuwa utaweza kuyapitia.",
                "Jipe fursa ya kujitunza, kwa sababu kila wakati unajitunza, unapata nguvu za kutosha.",
                "Hali ngumu hazidumu milele, lakini uwezo wako wa kuhimili ni wa kudumu.",
                "Kila kitu kina nafasi yake, na lazima uamini kuwa hata changamoto zako zina mwisho.",
                "Jifunze kuachilia baadhi ya vitu, kwa sababu sio kila kitu kinahitaji udhibiti wako.",
                "Unapohisi kuzidiwa, jua kwamba nguvu zako zimejijenga kupitia kila changamoto unayokutana nayo.",
                "Hakikisha unatoa nafasi kwa nafsi yako kupumzika na kuwa na amani.",
                "Usikate tamaa unapopitia magumu, kumbuka kuwa unajifunza kila siku.",
                "Kama unahisi msongo wa mawazo, jua kuwa kujitunza ni sehemu ya kuwa na nguvu."
                "Matatizo ya familia yanaweza kuwa na athari kubwa kwa akili na mwili wako. Kumbuka kuwa ni muhimu kujitunza wakati huu mgumu. Jaribu kufanya mazoezi ya kupumua ili kupunguza mvutano na uchovu. Pia, tafuta mtu wa kuzungumza naye, mtu anayekuelewa na kukupa ushauri wa busara. "
            ],
            "symptom": [
                "Jaribu mazoezi ya kupumua kwa kina ili kusaidia kupunguza mshituko wa mwili.",
                "Weka ratiba ya kupumzika ili kusaidia kupunguza uchovu unaosababishwa na msongo.",
                "Kuwa makini na mabadiliko ya mwili wako na chukua hatua za kujitunza mapema.",
                "Jitahidi kupata usingizi wa kutosha kusaidia mwili na akili yako kupata nafuu.",
                "Fanya shughuli unazopenda kama njia ya kupunguza maumivu ya kihisia.",
                "Tafuta mazingira tulivu unayoweza kujipa muda wa kutuliza akili yako.",
                "Usione aibu kutafuta msaada wa kitaalamu kama dalili za msongo zinaendelea.",
                "Punguza matumizi ya vifaa vya kidijitali kama simu au kompyuta ili kupumzisha akili.",
                "Fanya mazoezi mepesi kama kutembea kwa miguu ili kusaidia mwili kupunguza msongo.",
                "Kumbuka kuwa kusikiliza muziki kunaweza kupunguza dalili za msongo.",
                "Kama unahisi huzuni au maumivu, jaribu kutafuta wakati wa kupumzika na kufanya vitu vinavyokufurahisha.",
                "Unapohisi uchovu, tafadhali kumbuka kuwa kupumzika ni sehemu muhimu ya kujitunza.",
                "Jifunze kujisamehe unapohisi hasira au uchovu, kujitunza ni muhimu.",
                "Weka mipango ya kupumzika kila siku, hata kama ni kwa dakika chache.",
                "Jaribu kupunguza shinikizo la mawazo kwa kujitolea muda wa kuwa na amani.",
                "Kumbuka kuwa kufanya yoga au mazoezi ya kutuliza akili kunaweza kupunguza dalili za msongo.",
                "Usijali kuwa unahisi huzuni au msongo, kila mtu hupitia hayo katika nyakati ngumu.",
                "Fanya kazi kwa taratibu, usijali kwa sababu kila hatua ndogo inatoa mafanikio.",
                "Pumzika na kuzingatia hisia zako, ni njia nzuri ya kupunguza dalili za msongo.",
                "Fanya vitu vinavyokufurahisha ili kupunguza maumivu ya kihisia.",
                "Unapohisi kushindwa, jua kuwa ni muhimu kujitunza kwa usawa na kutafuta msaada inapohitajika.",
                "Hakuna shida kusema kwamba unahitaji mapumziko au msaada wa kitaalamu.",
                "Usijali kuhusu kila kitu, kumbuka kuwa unahitaji kujitunza ili kufurahi na kuwa na nguvu.",
                "Pumzika kutoka kwenye majukumu yako na tafuta mazingira ya utulivu.",
                "Unapohisi maumivu ya kihisia, jua kuwa kutafuta msaada ni ishara ya nguvu na kujali.",
                "Kama unahisi mwili wako umejaa msongo, jaribu kufanya mazoezi ya kutuliza akili.",
                "Kumbuka kuwa ni muhimu kuzingatia hisia zako na kutafuta nafasi ya kupumzika.",
                "Tafadhali kumbuka kuwa ni sawa kuwa na hisia ya msongo, lakini kujitunza ni muhimu.",
                "Kama unahisi umejaa shinikizo, pumzika na jaribu kufanya vitu vinavyokufurahisha.",
                "Kama unahisi uchovu mkubwa, jipe muda wa kupumzika na kuchukua mapumziko ya kweli.",
                "Jaribu kupunguza matumizi ya simu ili kusaidia akili yako kupumzika.",
                "Weka ratiba ya kupumzika kila siku ili kuzuia uchovu na msongo wa mawazo.",
                "Tafuta muda wa kutuliza akili yako kwa kufanya meditation au yoga.",
                "Pumzika kutoka kwa vitu vinavyokuongezea shinikizo na tafuta mazingira ya utulivu.",
                "Usijali kuhusu kila kitu unachohisi, ni sawa kuwa na hisia tofauti katika nyakati ngumu.",
                "Jifunze kutoa nafasi kwa nafsi yako kupumzika bila kujilaumu.",
                "Kama unahisi kupoteza mwelekeo, jaribu kupata muda wa kutuliza akili yako na kupumzika.",
                "Tafuta nafasi ya kutafakari na kupumzika, hata kama ni kwa muda mfupi.",
                "Usikate tamaa unapohisi kushindwa; pata muda wa kujitunza na kupata nguvu mpya.",
                "Kama unahisi uchovu, tafadhali tafuta mazingira ya kutuliza akili yako na kupumzika.",
                "Kumbuka kuwa kila hisia unayo hisi inahitajika kushughulikiwa kwa upole na kujali.",
                "Pumzika na usijali kwa sababu wewe ni muhimu na unahitaji kujitunza.",
                "Weka ratiba ya kupumzika ili kusaidia kupunguza dalili za msongo na kuchangamsha akili yako.",
                "Tafuta muda wa kujitunza kupitia vitu vinavyokufurahisha, kama kusikiliza muziki au kutembea.",
                "Jaribu kufanya kazi kwa polepole na kwa utulivu ili kupunguza msongo wa mwili na akili.",
                "Tafuta mazingira ya utulivu ambayo yatakusaidia kujitunza na kupata nguvu mpya.",
                "Fanya mazoezi ya kupumua kwa kina ili kupunguza athari za msongo na kufanya akili yako kuwa tulivu.",
                "Kumbuka kuwa si kila dalili ya msongo inahitaji kujibu kwa haraka, unahitaji pia kujitunza.",
                "Unapohisi huzuni, ni sawa kuchukua muda kutuliza akili yako na kuangalia mambo yanayokufurahisha.",
                "Usijali kuhusu kufanya kila kitu kwa haraka, hata hatua ndogo ni muhimu kwa afueni yako.",
                "Tafuta msaada wakati unahisi dalili za msongo kuwa kubwa ili kuepuka madhara ya kudumu.",
                "Pumzika kutoka kwa vitu vinavyokukera na tafuta shughuli zinazokufurahisha na kukupa nguvu."
            ],

            "intensity": [
                "Kama msongo unahisi kuwa mzito sana, tafadhali tafuta msaada wa haraka kutoka kwa mtaalamu.",
                "Unapohisi msongo kupita kiasi, jaribu kupumzika na kuweka akili yako kwenye shughuli tulivu.",
                "Hali ya hisia kali ni ya kawaida wakati mwingine, lakini ni muhimu kuitunza mapema.",
                "Kumbuka kwamba kuzungumza na mtu unayemuamini kunaweza kupunguza uzito wa hisia zako.",
                "Ukiona msongo unaathiri maisha yako ya kila siku, usisite kutafuta msaada wa kitaalamu.",
                "Jipe ruhusa ya kupumzika unapohisi umelemewa sana na hisia.",
                "Kumbuka kuwa si kila hali ya msongo inaweza kushughulikiwa peke yako; msaada ni muhimu.",
                "Fanya mazoezi mepesi au shughuli za kupumzisha mwili unapohisi msongo umekuwa mkubwa.",
                "Panga muda wa kujitunza kila siku ili kushughulikia msongo kabla haujazidi.",
                "Tafakari mafanikio madogo unayoyapata kila siku kama njia ya kupunguza uzito wa hisia zako.",
                "Unapohisi kuwa msongo umeongezeka, kumbuka kuwa ni sawa kutafuta msaada ili kusaidia kudhibiti hali.",
                "Kama hisia zako zinaonekana kuwa kali, ni muhimu kujitunza kwa upole na kuzingatia njia za kupumzika.",
                "Jipe ruhusa ya kupumzika kutoka kwa hali inayokusumbua ili kuepuka kuzidiwa na msongo.",
                "Unapohisi msongo mkubwa, chukua muda kufanya mazoezi au kutafuta mazingira ya amani.",
                "Kama hali inakuwa nzito, ni muhimu kutafuta msaada wa kitaalamu ili kusaidia kudhibiti hali hiyo.",
                "Jaribu kufikiria mambo mazuri ili kupunguza uzito wa mawazo yako na kupunguza msongo.",
                "Kama msongo unavyozidi, angalia mifumo ya kujitunza inayoweza kusaidia kubalance hali yako.",
                "Kama unahisi umejaa msongo, jaribu kupumzika na kufanya shughuli rahisi zinazokufurahisha.",
                "Kumbuka kuwa kila hatua ndogo inatoa faraja, hata ikiwa hali ya msongo inahisi kuwa kubwa.",
                "Jipe muda wa kupumzika mara kwa mara ili kukabiliana na msongo unaozidi kuathiri hali yako.",
                "Unapohisi kuwa hali inazidi kuwa mbaya, jaribu kujitolea muda wa kupumzika na kutuliza akili yako.",
                "Jua kuwa unapojitunza kila siku, unaweza kudhibiti na kupunguza madhara ya msongo wa mawazo.",
                "Pumzika kutoka kwa shughuli zinazokuletea msongo na tafuta muda wa kujitunza.",
                "Kama hali inakuwa ngumu sana, usikate tamaa, tafuta msaada wa kitaalamu ili kusaidia kuhamasisha mabadiliko.",
                "Kumbuka kuwa hakuna aibu kutafuta msaada unapohisi msongo unaathiri uwezo wako wa kufanya mambo ya kila siku.",
                "Jaribu kutafuta shughuli rahisi za kupunguza hisia kali za msongo, kama kusikiliza muziki au kufanya yoga.",
                "Hakikisha kuwa unapata muda wa kupumzika kutoka kwa majukumu yako ya kila siku ili kupunguza msongo.",
                "Pumzika na ujitunze, unapohisi msongo mkubwa, ni muhimu kujitahidi kubaki na utulivu.",
                "Unapohisi msongo unavyoongezeka, fikiria kufanya mazoezi ya kupumua kwa kina ili kusaidia kupunguza athari zake.",
                "Kama hali ya msongo inavyozidi, tafadhali angalia njia za kupunguza kasi yake na kutafuta msaada.",
                "Kumbuka kuwa msongo mkubwa unaweza kushughulikiwa kwa njia mbalimbali, ikiwa ni pamoja na kujitunza na kutafuta msaada.",
                "Kama unahisi kuwa msongo unakufinya, ni wakati mzuri wa kutafuta njia za kupumzika na kutoa nafasi kwa nafsi yako.",
                "Pumzika, hata kama ni kwa dakika chache, ili kupunguza athari za msongo mkubwa.",
                "Kumbuka kuwa unahitaji kujitunza kila siku ili kupunguza hatari ya msongo mkubwa.",
                "Kama unahisi kuwa hali ya msongo inaathiri kila kitu unachofanya, tafadhali tafuta msaada wa kitaalamu ili kusaidia kudhibiti hali.",
                "Fanya mazoezi ya mwili au tafuta mazingira tulivu ili kupunguza hali ya msongo unaozidi.",
                "Usijali kuhusu kila kitu unachohisi, unapohisi msongo mkubwa, ni muhimu kutafuta msaada na kupumzika.",
                "Jaribu kuchukua muda kwa ajili ya kujitunza ili kupunguza athari za msongo mkubwa.",
                "Kama unahisi hali ya msongo inakwenda mbali zaidi, tafuta mtu unayemwamini ili kuzungumza kuhusu hisia zako.",
                "Unapohisi kuwa msongo unakuwa mzito, tafuta aina ya kujitunza inayoweza kusaidia kupunguza dalili.",
                "Usione aibu kutafuta msaada wa kitaalamu wakati hali ya msongo inazidi kuwa kubwa.",
                "Kama hisia zako zinakuwa kali na unahisi kuwa msongo unakuwa mkubwa, tafuta muda wa kutuliza akili yako.",
                "Kumbuka kuwa ni muhimu kujitunza ili kupunguza athari za msongo kubwa kwa mwili na akili yako.",
                "Pumzika na unyenyekevu unapohisi msongo mkubwa, hata hatua ndogo inaweza kusaidia.",
                "Jipe muda wa kutuliza akili yako ikiwa hali ya msongo inakufinya, hii ni njia nzuri ya kupunguza hisia kali.",
                "Kama unahisi kuwa msongo unakuletea madhara makubwa, tafuta msaada wa kitaalamu ili kusaidia kudhibiti hali."
            ]

        }
        if stress_issues:
            response = []
            for issue in stress_issues:
                advice_part = random.choice(advice[issue])
                response.append(f" {advice_part}")
            first_response = "Pole kwa unayopitia, najua hali hii inaweza kuwa ngumu lakini niko hapa kwa ajili yako. "
            full_response = first_response + " ".join(response)  # Join the response without the first part
            dispatcher.utter_message(full_response.strip())

        else:
            dispatcher.utter_message("tafadhali unaweza kunieleza zaidi,niko hapa kwa ajili yako.")
            return [SlotSet(slot, None) for slot in stress_issues]



class ActionLoneliness(Action):
    def name(self):
        return "action_loneliness"
    def run(self, dispatcher, tracker, domain):
        lonely_issues={}
        for slot in ["feeling", "cause"]:
            value = tracker.get_slot(slot)
            if value:
                lonely_issues[slot]=value
        loneliness_advice={"feeling": [
                "Pole sana kwa kile unachohisi, upweke unaweza kuwa mzito na mgumu kushughulikia.",
                "Kama unajihisi kupotea, kumbuka kuwa kuna watu wanaojali na wako tayari kukusaidia.",
                "Wakati mwingine hisia za upweke zinaweza kuwa ngumu kuelezea, lakini usijione peke yako.",
                "Ni sawa kuhisi huzuni na upweke, kila mtu hupitia hali kama hiyo wakati mwingine.",
                "Kama unahisi umepoteza njia, tafuta msaada kutoka kwa mtu unayemwamini. Usikate tamaa.",
                "Najiunga na wewe katika maombi ya kuwa na amani katika moyo wako. Upweke unahisi kama mzigo mkubwa.",
                "Kama unahisi kuwa huwezi kushirikiana na wengine, tafuta njia ndogo za kujiunganishia na watu.",
                "Kumbuka, hisia zako ni sahihi na unastahili kujaliwa na wengine.",
                "Upweke unaweza kufanywa kuwa mwepesi kwa hatua ndogo za kushirikiana na wengine.",
                "Jua kuwa hisia zako ni muhimu na zinapaswa kuzingatiwa. Upweke hauwezi kukufanya kuwa dhaifu.",
                "Kama unapitia magumu, tafuta msaada bila aibu. Si lazima uhisi upweke kila wakati.",
                "Inahitaji nguvu kubwa kukabiliana na upweke, lakini kujua kwamba kuna wengine wanaojali kunaweza kusaidia.",
                "Hakuna makosa katika kuhisi huzuni au upweke. Hii ni sehemu ya maisha na kila mmoja wetu anapitia hilo.",
                "Pole sana, najua ni vigumu lakini unaweza kushinda hali hii kwa msaada na kujitunza mwenyewe.",
                "Wakati mwingine, kutafuta mtu wa kuzungumza naye kunaweza kupunguza uzito wa upweke.",
                "Usijione peke yako, kuna watu wanaojali na wako tayari kukusaidia kutatua hisia hizi.",
                "Kama upweke unakukalia, tafuta njia ndogo ya kujihusisha na jamii au marafiki.",
                "Jua kwamba upweke ni hisia ya kawaida, lakini si lazima iwe sehemu ya maisha yako milele.",
                "Kama unajihisi upweke, angalia mifumo ya kujitunza inayoweza kusaidia kuboresha hali yako.",
                "Kumbuka, kuna nguvu kubwa katika kushirikiana na wengine, hata kama ni hatua ndogo.",
                "Tafadhali usikate tamaa, upweke utapita na kuna watu wanaokusudia kukusaidia katika kipindi hiki.",
                "Pole sana kwa kile unachohisi, lakini kumbuka kila changamoto ina mwisho, na hii pia itapita.",
                "Kama unahisi upweke, jaribu kuzungumza na mtu unayemwamini, hiyo inaweza kupunguza hisia zako.",
                "Jua kwamba kuna watu duniani wanaokujali na wapo tayari kutusaidia kwa njia yoyote ile.",
                "Hakuna aibu katika kuhisi upweke. Wengi wetu tunapitia hiyo na ni sehemu ya maisha.",
                "Pole kwa kile unachohisi. Kumbuka kwamba upweke ni hali ya kupita, na kuna njia za kujitunza ili kupunguza athari zake.",
                "Usijione peke yako, kuna watu wanaowajali na wako tayari kusaidia unapohitaji msaada.",
                "Jaribu kutafuta mambo madogo yanayoweza kuboresha hali yako, kama kutafuta mazungumzo ya kirafiki au kuchukua muda kwa ajili yako mwenyewe.",
                "Kama unahisi kupoteza, kumbuka kwamba kila mtu hupitia upweke kwa wakati fulani na hiyo si kasoro.",
                "Kama unahisi upweke, tafuta vitu vinavyoweza kukufanya ujisikie vizuri, kama kufanya shughuli zinazokufurahisha.",
                "Unapojisikia upweke, tafuta nafasi ya kutoa hisia zako kwa mtu unayemwamini.",
                "Jua kwamba hisia zako ni sahihi, lakini pia kuna watu wanaoweza kukusaidia kupitia kipindi hiki.",
                "Kama upweke unakulemea, tafuta msaada wa marafiki au familia yako ili upate msaada wa kihisia.",
                "Pole sana kwa kile unachohisi, lakini kumbuka kwamba kila hisia ina sababu na kila hali ina mwisho.",
                "Kama unahisi kuwa umeachwa peke yako, tafuta msaada kutoka kwa wale wanaokujali na wanaweza kusaidia.",
                "Hakuna aibu katika kutafuta msaada unapohisi upweke, na unastahili kupata upendo na msaada.",
                "Tafuta njia ndogo za kushirikiana na wengine, kama kuzungumza na mtu au kufanya shughuli za kijamii.",
                "Usijione peke yako, kuna jamii nyingi zinazokusaidia kupunguza hisia za upweke.",
                "Pole kwa kile unachohisi, lakini kumbuka kuwa upweke unaweza kupunguza kwa hatua ndogo za kutafuta msaada.",
                "Kama unahisi upweke, tafuta fursa za kuungana na wengine kwa njia ya mtandao au kwa familia na marafiki.",
                "Jua kwamba hisia zako ni halali, na kuna watu wengi ambao wanapitia hali kama hiyo.",
                "Kama unahisi kupotea, kumbuka kwamba wewe ni muhimu na kuna watu wanaokujali na wanataka kuona ukiishi vizuri.",
                "Jipe muda wa kuzungumza na mtu, kama unahisi upweke. Hii inaweza kupunguza hali ya kujihisi peke yako.",
                "Hata wakati unajihisi upweke, kumbuka kwamba kuna wengine wanatamani kukusaidia, na hakuna ubaya kutafuta msaada.",
                "Upweke unaweza kuwa ngumu, lakini hatua ndogo kama kuzungumza na mtu anaweza kubadili hisia zako.",
                "Kama unahisi upweke, tafuta huduma au msaada wa kitaalamu ili kupunguza athari zake.",
                "Pole kwa kile unachohisi, lakini kumbuka kwamba kila mtu hupitia wakati wa upweke, na unaweza kushinda hili kwa msaada.",
                "Kama hisia zako za upweke zinaendelea, tafuta njia za kuungana na wengine kama njia ya kupunguza hali hiyo.",
                "Upweke ni hali ya kawaida, na kuna watu wengi ambao wanaweza kusaidia kupunguza athari zake.",
                "Pole kwa kile unachohisi, lakini kumbuka kwamba kila hali ina mwisho, na upweke hautadumu milele."
            ],
            "cause": [
                "Unapohisi kutengwa, inaweza kuwa ni matokeo ya mabadiliko katika maisha yako. Jaribu kufungua moyo kwa wengine.",
                "Kukosa uhusiano wa karibu na watu wengine kunaweza kusababisha hali ya upweke. Tafuta fursa ya kuungana na wengine.",
                "Wakati mwingine, upweke unatokana na kupoteza mtu wa karibu. Hali hii inaweza kuachia maumivu, lakini jipe muda na usihisi aibu kutafuta msaada.",
                "Kama unajihisi mbali na jamii yako, tafuta njia za kujumuika na wengine au kuanzisha mazungumzo na watu wapya.",
                "Upweke unaweza kuwa matokeo ya kutokuwa na shughuli zinazoendana na masilahi yako. Tafuta njia ya kujishughulisha na vitu unavyovipenda.",
                "Kama umepitia mabadiliko makubwa ya maisha kama kuhamia sehemu mpya, unaweza kujihisi kutengwa. Hata hivyo, mambo yanaweza kubadilika kwa wakati.",
                "Kukosa uhusiano wa karibu na familia au marafiki kunaweza kuwa chanzo cha upweke. Hakikisha unajitahidi kuwasiliana nao mara kwa mara.",
                "Pia, kukosa uhusiano wa kimapenzi kunaweza kuleta hisia za upweke. Kumbuka, unapohitaji, unaweza kutafuta msaada kutoka kwa marafiki.",
                "Kama umejichagua kuwa na maisha ya faragha au kujitenga, upweke unaweza kujitokeza kwa urahisi. Tafuta njia za kujumuika na wengine.",
                "Mabadiliko katika kazi au masomo yanaweza kusababisha upweke. Punguza mzigo kwa kushirikiana na wengine kwenye shughuli zinazofanana.",
                "Kutokuwa na shughuli zinazokufurahisha kunaweza kusababisha hali ya upweke. Tafuta vitu vinavyokuvutia na unavyopenda kufanya.",
                "Ikiwa unahisi kupoteza lengo au mwelekeo katika maisha, unaweza kujikuta ukiwa na upweke. Jaribu kutafuta msukumo kutoka kwa wale wanaokuzunguka.",
                "Kama unajihisi kutengwa kutokana na imani au maadili yako, tafuta watu wenye mtazamo sawa ili kujenga uhusiano.",
                "Unapohisi kuwa huna kitu cha kufanya au kuzungumza, upweke unaweza kujitokeza. Tafuta shughuli za kujieleza au kujifunza vitu vipya.",
                "Hali ya upweke inaweza kuletwa na kutokuwa na msaada wa kihisia kutoka kwa wengine. Hakikisha unatafuta watu wa kukusaidia wakati mgumu.",
                "Upweke unaweza kutokea unapohisi kwamba hakuna mtu wa kuelewa hali yako. Tafuta watu wanaoweza kukusaidia kujielewa.",
                "Mabadiliko ya kijamii yanaweza kuchangia hali ya upweke. Tafuta njia ya kujumuika na watu wapya ili kuimarisha hisia zako za kutokuwa peke yako.",
                "Kama unahisi kupoteza mtu wa karibu, inaweza kuleta hali ya upweke. Jipe muda na tafuta msaada kwa wale wanaoweza kusaidia.",
                "Wakati mwingine, hali ya upweke inaweza kutokana na kutokuwa na majukumu au malengo. Tafuta shughuli au kazi zinazokufaa.",
                "Kama umehamia sehemu mpya au kufanya mabadiliko makubwa katika maisha yako, upweke unaweza kuonekana. Hata hivyo, mambo yataanza kuwa bora kwa wakati.",
                "Kama unahisi kutengwa kutokana na tofauti za kisiasa au kijamii, tafuta watu wanaoshiriki maoni yako ili kujenga ushirikiano.",
                "Upweke unaweza kutokana na kutokuwa na uhusiano wa kijamii. Tafuta fursa ya kuungana na wengine na kujijengea jamii yenye msaada.",
                "Mabadiliko katika familia au mazingira yako yanaweza kuleta hali ya upweke. Tafuta msaada kutoka kwa watu wa karibu ili kushughulikia hali hii.",
                "Kama unahisi upweke kutokana na changamoto za kiuchumi au kazi, jaribu kutafuta msaada wa kijamii na familia.",
                "Hali ya upweke inaweza kuwa matokeo ya kutokuwa na vipaumbele au malengo katika maisha yako. Tafuta fursa mpya za kujishughulisha.",
                "Upweke unaweza kutokea unapohisi kutokuwa na shabiki au watu wanaokuelewa. Tafuta fursa za kuungana na watu wenye maslahi sawa.",
                "Kama unahisi kupoteza mtazamo kuhusu maisha yako, upweke unaweza kuonekana. Tafuta msaada kutoka kwa wale wanaokujali ili kupata mtazamo mpya.",
                "Kama unahisi kutokuwa na uhusiano wa kihisia na wengine, tafuta njia za kujitunza na kuungana na jamii yako.",
                "Unapohisi kutokuwa na mazungumzo ya maana, upweke unaweza kuzidi. Tafuta nafasi za kujifunza na kushirikiana na wengine.",
                "Kama unahisi kutengwa kwa sababu ya mabadiliko ya maisha yako, jaribu kutafuta njia ya kujitunza na kujenga uhusiano mpya.",
                "Upweke unaweza kuletwa na kukosa mtu wa karibu anayeweza kukusaidia. Tafuta msaada kutoka kwa marafiki na familia.",
                "Kutokuwa na ratiba ya shughuli za kijamii kunaweza kusababisha hali ya upweke. Tafuta fursa za kushirikiana na wengine.",
                "Kama upweke unakukalia kutokana na kutokuwa na uhusiano wa kimapenzi, tafuta njia za kuungana na watu au kujihusisha na shughuli.",
                "Mabadiliko katika kazi au shule yanaweza kuleta hali ya upweke. Tafuta msaada kutoka kwa wenzako ili kushirikiana na wao.",
                "Unapohisi kutokuwa na msaada wa kihisia, upweke unaweza kuwa mzito. Tafuta msaada kutoka kwa wataalamu au jamii yako.",
                "Upweke unaweza kutokana na kutokuwa na hamu ya kufanya vitu au kushirikiana na wengine. Tafuta vitu vinavyokuvutia na kufanya hatua ndogo.",
                "Kama unahisi kupoteza msukumo, upweke unaweza kuwa sehemu ya hiyo. Tafuta msaada na ushirikiano kutoka kwa wengine.",
                "Kama unajihisi kutengwa au kupoteza mwelekeo, tafuta msaada ili kujipata upya na kujitunza vizuri.",
                "Upweke unaweza kutokea unapohisi kutokuwa na shabiki au mtu anayekuelewa. Tafuta njia ya kujihusisha na watu na kujenga jamii.",
                "Kama umehamia mahali pasipo familia au marafiki, upweke unaweza kuwa changamoto. Tafuta njia za kujitunza na kujenga uhusiano mpya.",
                "Kama unajihisi kutengwa kutokana na kutokuwa na maslahi yanayofanana na wengine, tafuta jamii inayoshiriki maslahi sawa.",
                "Kama hali ya upweke inahusiana na matatizo ya kifamilia, tafuta msaada wa kihisia kutoka kwa watu wa karibu au wataalamu.",
                "Kama unahisi kutengwa au kukosa mtu wa kujali, tafuta njia za kuungana na wengine na kujijenga upya."
            ]

        }
        if lonely_issues:
            responses=[]
            for issues in lonely_issues:
                advice_parts = random.choice(loneliness_advice[issues])
                responses.append(f" {advice_parts}")
            first_part = "Pole kwa unayopitia,kumbuka huyuko pekee yako nko hapa kwa ajili yako."
            full_response = first_part + " ".join(responses)  # Join the response without the first part
            dispatcher.utter_message(full_response.strip())

        else :
            dispatcher.utter_message("tafadhali unaweza kunieleza zaidi,niko hapa kwa ajili yako.")
            return [SlotSet(slot, None) for slot in lonely_issues]