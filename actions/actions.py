from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random
import re
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker


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



#drug abuse advice
class ActionDrugAbuseAdvice(Action):
    def name(self):
        return "action_drug_abuse_advice"

    def run(self, dispatcher, tracker, domain):
        detected_issues = {}
        for slot in ["drug_use", "coping_mechanism", "peer_influence", "emotional_state", "negative_impact"]:
            value = tracker.get_slot(slot)
            if value:
                detected_issues[slot] = value

        advice_map = {
            "drug_use": [
                "Asante kwa kushiriki kuhusu matumizi ya dawa. Kujua hali yako ni sehemu muhimu ya kuchunguza njia bora za kujisaidia.",
                "Matumizi ya dawa yanaweza kuwa sehemu ya maisha kwa sababu tofauti, na ni jambo zuri kuweza kuangalia hatua unazoweza kuchukua ili kujiboresha.",
                "Ni hatua ya ujasiri kuzungumzia matumizi ya dawa. Tunaweza kuangalia njia salama za kukusaidia kutimiza malengo yako ya kiafya na ustawi."
            ],
            "peer_influence": [
                "Ni kawaida mtu kuanza kutumia dawa za kulevya kutokana na ushawishi wa marafiki. Ni jambo ambalo linaweza kutokea bila hata kuliona mapema.",
                "Matumizi ya dawa za kulevya yanaweza kuanza kwa presha kutoka kwa marafiki, jambo ambalo wengi wamepitia katika maisha yao.",
                "Wakati mwingine, ushawishi wa watu wa karibu unaweza kuwa sababu ya kuanza kutumia dawa za kulevya bila kutarajia.",
                "Ushawishi wa marafiki umechangia katika safari yako ya matumizi ya dawa za kulevya, hali ambayo ni ya kawaida na inaeleweka."
            ],
            "emotional_state": [
                "Wakati mwingine, hali ya kihisia inayomwelemea mtu inaweza kuchangia kuanza kutumia dawa za kulevya. Ni jambo linalotokea kwa watu wengi katika maisha.",
                "Matumizi ya dawa za kulevya yanaweza kuwa majibu kwa hisia ngumu mtu anazopitia, jambo ambalo ni la kawaida kueleweka.",
                "Kukumbwa na changamoto za kihisia kunaweza kumfanya mtu aanze kutumia dawa za kulevya kama njia ya kujituliza kwa muda.",
                "Hisia nzito kama huzuni, hasira au upweke zinaweza kuwa sababu ya mtu kujaribu kutumia dawa za kulevya ili kukabiliana na hali hiyo.",
            ],
            "enjoyment": [
                "Wakati mwingine, mtu huanza kutumia dawa za kulevya kwa kutafuta burudani au hisia za furaha, jambo ambalo linaeleweka katika hali fulani za maisha.",
                "Kutumia dawa za kulevya kwa ajili ya kupata starehe ni hali inayopatikana kwa watu wengi, hasa wanapohitaji hisia za faraja au msisimko.",
                "Matumizi ya dawa za kulevya yanaweza kuonekana kama njia ya kuongeza starehe au kuboresha hisia za muda mfupi, hali ambayo ni ya kawaida kwa baadhi ya watu.",
                "Kutafuta furaha au kubadili hisia kunaweza kuwa sababu iliyokupelekea kuanza kutumia dawa za kulevya, hali inayotokea kwa watu wengi kwa nyakati tofauti."
            ],
            "negative_impact": [
                "Matumizi ya dawa za kulevya yanaweza kuleta athari hasi katika nyanja mbalimbali za maisha, hali ambayo wengi wamewahi kukumbana nayo.",
                "Ni kawaida kuona kwamba matumizi ya dawa za kulevya yanaathiri maisha ya mtu kwa njia tofauti, na ni muhimu kulitambua hilo.",
                "Madhara yanayosababishwa na matumizi ya dawa za kulevya yanaweza kuathiri maisha ya kijamii, kiafya au kisheria, jambo linalotokea kwa watu wengi.",
                "Kutambua athari hasi zinazotokana na matumizi ya dawa za kulevya ni hatua muhimu kuelekea kuelewa hali halisi ya maisha yako."
            ]
        }

        if detected_issues:
            response_parts = []
            for issue in detected_issues:
                if issue in advice_map:
                    advice = random.choice(advice_map[issue])
                    response_parts.append(f" **{issue.capitalize()}**: {advice}")

            response = "Naelewa hali yako na hapa kuna ushauri:\n\n" + "\n".join(response_parts)
            dispatcher.utter_message(response.strip())
        else:
            dispatcher.utter_message("Naomba unieleze zaidi ili niweze kusaidia vyema.")

        return [SlotSet(slot, None) for slot in detected_issues] #Reset slots after response

#family relationship advice
class ActionFamilyRelationshipAdvice(Action):
    def name(self):
        return "action_family_relationship_advice"

    def run(self, dispatcher, tracker, domain):
        detected_issues = {}
        for slot in ["family_expectations", "family_conflict", "family_neglect", "family_separation",
                     "family_control"]:
            value = tracker.get_slot(slot)
            if value:
                detected_issues[slot] = value

        advice_map = {
            "family_expectations": [
                "Matarajio kutoka kwa familia yanaweza kuwa chanzo cha changamoto katika mahusiano ya kifamilia, hali inayowapata watu wengi.",
                "Mara nyingi, shinikizo la kukidhi matarajio ya kifamilia linaweza kusababisha migogoro au msongo wa mawazo katika mahusiano ya familia.",
                "Changamoto zinazotokana na matarajio ya familia ni sehemu halisi ya matatizo ya mahusiano ya kifamilia ambayo watu wengi hukumbana nayo.",
                "Ni kawaida kujikuta ukikabiliwa na matatizo ya kifamilia yanayohusiana na matarajio makubwa au matarajio yasiyoeleweka vizuri."
            ],
            "family_conflict": [
                "Migogoro ya kifamilia ni sehemu inayochangia kwa kiasi kikubwa changamoto za mahusiano ya kifamilia, hali ambayo watu wengi hupitia katika maisha.",
                "Ni kawaida mahusiano ya kifamilia kukumbwa na mivutano na kutokuelewana, hali inayoweza kuathiri mshikamano wa familia.",
                "Changamoto za mahusiano ya kifamilia mara nyingi hutokana na migogoro ndani ya familia, jambo ambalo ni la kawaida katika mazingira mbalimbali.",
                "Kutokea kwa migongano na kutoelewana ndani ya familia ni sehemu halisi ya matatizo ya mahusiano ya kifamilia ambayo wengi hukumbana nayo."
            ],
            "family_neglect": [
                "Matatizo ya mahusiano ya kifamilia mara nyingi huweza kuathiriwa na hali ya kutengana ndani ya familia, jambo ambalo ni la kawaida kutokea.",
                "Kutengana kwa wanafamilia kunaweza kuleta changamoto kubwa katika mahusiano ya kifamilia, hali inayowagusa watu wengi kwa njia tofauti.",
                "Changamoto nyingi za mahusiano ya kifamilia zinaweza kuchochewa na hali ya familia kutengana, iwe kihisia au kimazingira.",
                "Ni kawaida kwa matatizo ya kifamilia kuongezeka pale ambapo kunakuwepo na hali ya kutengana au kuvunjika kwa uhusiano wa kifamilia."
            ],
            "family_separation": [
                "Changamoto nyingi katika mahusiano ya kifamilia zinaweza kutokana na hali ya udhibiti mkubwa kutoka kwa wanafamilia, jambo ambalo ni la kawaida katika baadhi ya familia.",
                "Ni kawaida mtu kujikuta akikumbwa na matatizo ya kifamilia yanayosababishwa na udhibiti wa kupindukia kutoka kwa watu wa familia.",
                "Hali ya kutokuwa na uhuru wa kufanya maamuzi binafsi ndani ya familia inaweza kuchangia matatizo katika mahusiano ya kifamilia.",
                "Migogoro ya kifamilia inaweza kuongezeka pale ambapo udhibiti wa familia unazuia uhuru wa kujiamulia mambo binafsi."

            ],
            "family_control": [
                "Matatizo ya mahusiano ya kifamilia mara nyingi huathiriwa na hali ya kupuuzwa au kutopata uangalizi kutoka kwa wanafamilia.",
                "Ni kawaida mtu kujikuta akikumbwa na changamoto za kifamilia zinazosababishwa na hisia za kupuuzwa na familia yake.",
                "Kutopata msaada wa kihisia au kimaendeleo kutoka kwa familia kunaweza kuchangia matatizo katika mahusiano ya kifamilia.",
                "Kupitia hali ya kupuuzwa na familia ni sehemu halisi ya matatizo ya kifamilia ambayo watu wengi huathirika nayo katika maisha yao."
            ]
        }

        if detected_issues:
            response_parts = []
            for issue in detected_issues:
                if issue in advice_map:
                    advice = random.choice(advice_map[issue])
                    response_parts.append(f" **{issue.capitalize()}**: {advice}")

            response = "Naelewa hali yako na hapa kuna ushauri:\n\n" + "\n".join(response_parts)
            dispatcher.utter_message(response.strip())
        else:
            dispatcher.utter_message("Naomba unieleze zaidi ili niweze kusaidia vyema.")

        return [SlotSet(slot, None) for slot in detected_issues] #Reset slots after response

#romantic relationship advice
class ActionRomanticRelationshipAdvice(Action):
    def name(self):
        return "action_romantic_relationship_advice"

    def run(self, dispatcher, tracker, domain):
        detected_issues = {}
        for slot in ["romantic_trust_and_jealousy", "romantic_communication_issues",
                     "romantic_conflict", "romantic_affection_and_attention", "romantic_control"]:
            value = tracker.get_slot(slot)
            if value:
                detected_issues[slot] = value

        advice_map = {
            "romantic_trust_and_jealousy": [
                "Changamoto katika mahusiano ya kimapenzi mara nyingi huweza kuchochewa na matatizo ya kuaminiana au wivu, hali inayowapata watu wengi.",
                "Ni kawaida kwa matatizo ya kimapenzi kuibuka pale ambapo kuna ukosefu wa uaminifu au hisia za wivu kati ya wenzi.",
                "Mahusiano ya kimapenzi yanaweza kuathiriwa sana na changamoto zinazohusiana na uaminifu na wivu, jambo ambalo ni la kawaida katika uhusiano wa karibu.",
                "Migogoro ya kimapenzi mara nyingi hutokana na hisia za kutoaminiana au wivu, hali ambayo wengi hukumbana nayo katika safari ya mahusiano."
            ],
            "romantic_communication_issues": [
                "Changamoto katika mawasiliano ni sababu ya kawaida ya matatizo katika mahusiano ya kimapenzi, hali inayowapata watu wengi katika safari ya mapenzi.",
                "Ni kawaida kuona mahusiano ya kimapenzi yakikumbwa na matatizo kutokana na ukosefu wa mawasiliano wazi na yenye kuelewana.",
                "Migogoro katika mahusiano ya kimapenzi mara nyingi huanzia kwenye changamoto za mawasiliano kati ya wenzi.",
                "Mahusiano ya kimapenzi yanaweza kuathiriwa kwa kiasi kikubwa na mawasiliano yasiyofaa, jambo ambalo ni la kawaida kwa watu wengi wanaopitia changamoto za mapenzi."
            ],
            "romantic_conflict": [
                "Migogoro ndani ya mahusiano ya kimapenzi ni sehemu ya changamoto nyingi zinazowakumba watu katika safari ya mapenzi.",
                "Ni kawaida kwa mahusiano ya kimapenzi kukumbwa na migogoro na kutokuelewana, hali inayoweza kuathiri ukaribu kati ya wenzi.",
                "Matatizo katika mahusiano ya kimapenzi mara nyingi huongezeka pale ambapo migogoro ya mara kwa mara haishughulikiwi ipasavyo.",
                "Migongano ya kimapenzi ni sehemu ya changamoto za mahusiano ambazo watu wengi hukumbana nazo katika safari ya kujenga uhusiano wa karibu."
            ],
            "romantic_affection_and_attention": [
                "Upungufu wa upendo na uangalizi katika mahusiano ya kimapenzi ni moja ya changamoto zinazoweza kuathiri uhusiano kati ya wenzi.",
                "Ni kawaida kwa matatizo ya kimapenzi kuibuka pale ambapo mtu anahisi kutopokea mapenzi au uangalizi wa kutosha kutoka kwa mwenzi wake.",
                "Changamoto katika mahusiano ya kimapenzi mara nyingi hutokana na hisia za kutopata mapenzi ya kutosha au kutojaliwa kwa kiwango kinachohitajika.",
                "Mahusiano ya kimapenzi yanaweza kukumbwa na changamoto kubwa pale ambapo kuna ukosefu wa hisia za upendo na uangalizi wa karibu."
            ],
            "romantic_control": [
                "Udhibiti mkubwa katika mahusiano ya kimapenzi ni moja ya sababu zinazoweza kuchangia changamoto kubwa kati ya wenzi.",
                "Ni kawaida kwa mahusiano ya kimapenzi kukumbwa na matatizo pale ambapo mmoja wa wenzi anahisi kupokonywa uhuru wake binafsi.",
                "Changamoto katika mahusiano ya kimapenzi mara nyingine huongezeka pale ambapo kuna hisia za kudhibitiwa kupita kiasi.",
                "Mahusiano ya kimapenzi yanaweza kuathiriwa kwa kiasi kikubwa na hali ya udhibiti, hali inayowapata watu wengi wanaopitia changamoto za mapenzi."
            ]
        }

        if detected_issues:
            response_parts = []
            for issue in detected_issues:
                if issue in advice_map:
                    advice = random.choice(advice_map[issue])
                    response_parts.append(f" **{issue.capitalize()}**: {advice}")

            response = "Naelewa hali yako na hapa kuna ushauri:\n\n" + "\n".join(response_parts)
            dispatcher.utter_message(response.strip())
        else:
            dispatcher.utter_message("Naomba unieleze zaidi ili niweze kusaidia vyema.")

        return [SlotSet(slot, None) for slot in detected_issues] #Reset slots after response


