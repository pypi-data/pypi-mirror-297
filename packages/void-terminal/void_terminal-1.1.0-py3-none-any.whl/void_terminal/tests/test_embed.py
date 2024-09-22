def validate_path():
    import os, sys
    os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(os.path.dirname(__file__) + "/..")
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)

validate_path()  # validate path so you can run from base directory

# # """
# # Test 1
# # """

# # from request_llms.embed_models.openai_embed import OpenAiEmbeddingModel
# # from shared_utils.connect_void_terminal import get_chat_default_kwargs
# # oaiem = OpenAiEmbeddingModel()

# # chat_kwargs = get_chat_default_kwargs()
# # llm_kwargs = chat_kwargs['llm_kwargs']
# # llm_kwargs.update({
# #     'llm_model': "text-embedding-3-small"
# # })

# # res = oaiem.compute_embedding("Hello", llm_kwargs)
# # print(res)

# """
# Test 2
# """

# from request_llms.embed_models.openai_embed import OpenAiEmbeddingModel
from void_terminal.shared_utils.connect_void_terminal import get_chat_default_kwargs
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from crazy_functions.rag_fns.vector_store_index import GptacVectorStoreIndex
# from llama_index.core.ingestion import run_transformations
# from llama_index.core import PromptTemplate
# from llama_index.core.response_synthesizers import TreeSummarize

# # NOTE: we add an extra tone_name variable here
# DEFAULT_QUESTION_GENERATION_PROMPT = """\
# Context information is below.
# ---------------------
# {context_str}
# ---------------------
# Given the context information and not prior knowledge.
# generate only questions based on the below query.
# {query_str}
# """


chat_kwargs = get_chat_default_kwargs()
llm_kwargs = chat_kwargs['llm_kwargs']
llm_kwargs.update({
    'llm_model': "text-embedding-3-small",
    'embed_model': "text-embedding-3-small"
})
# embed_model = OpenAiEmbeddingModel(llm_kwargs)

# ## dir
# documents = SimpleDirectoryReader("private_upload/rag_test/").load_data()

# ## single files
# # from llama_index.core import Document
# # text_list = [text1, text2, ...]
# # documents = [Document(text=t) for t in text_list]
# vsi = GptacVectorStoreIndex.default_vector_store(embed_model=embed_model)
# documents_nodes = run_transformations(
#                         documents,  # type: ignore
#                         vsi._transformations,
#                         show_progress=True
#                     )
# index = vsi.insert_nodes(documents_nodes)
# retriever = vsi.as_retriever()

# query = "what is core_functional.py"

# res = retriever.retrieve(query)
# context_str = '\n'.join([r.text for r in res])
# query_str = query
# query = DEFAULT_QUESTION_GENERATION_PROMPT.format(context_str=context_str, query_str=query_str)
# print(res)
# print(res)


# # response = query_engine.query("Some question about the data should go here")
# # print(response)

from void_terminal.crazy_functions.rag_fns.llama_index_worker import LlamaIndexRagWorker
rag_worker = LlamaIndexRagWorker('good-man-user', llm_kwargs, checkpoint_dir='./longlong_vector_store')

rag_worker.add_text_to_vector_store("""
Bear child.（Cotyledon tomentosa）Is the Crassulaceae family，Perennial succulent herbaceous plants of the genus Silver Wave，Plants have multiple branches，The stem is green.，The fleshy leaves are thick.，Mutual interaction for life，Oval shape，Green，Dense white short hair.。The leaf tips have red claw-like teeth，Dichasial umbel，Small yellow flowers，Flowering period is July to September。
This type originated in the Cape Province of South Africa.。Prefers warm and dry conditions.，Plenty of sunshine，Well-ventilated environment。Excessively high summer temperatures will cause dormancy.。Avoid cold and excessive humidity。Propagation methods include cuttings。
This type of leaf shape and color is more beautiful，The flowers are exquisite and delicate，The leaves resemble the paws of a small bear.，The form is peculiar.，Very lovely.，High aesthetic value。
Species index：IN4679748
""")

rag_worker.add_text_to_vector_store("""
The jade ring is from the genus Crassula in the Crassulaceae family [4]Perennial succulent herbaceous plants。 [5]The surface of the green halo leaves has a translucent granularity，Crystal clear; two cylindrical leaves，In the early stages of growth, like rabbit ears.，Very lovely，As they grow, the leaves will gradually become longer and thicker，Easily droops when lacking water; has branches.，Yi Qunsheng.。
The blue halo originates from South Africa。Bright blue light enjoys a warm and well-diffused environment.，More cold-resistant，Avoid strong sunlight exposure.，The summer heat dormancy is obvious。 [6]The propagation methods of the green halo include cuttings and sowing。 [7]
The small, plump, and round appearance of the jade ring is very cute.，Looks like a little rabbit with long ears，The cute appearance makes people unable to put it down，And it`s not difficult to sustain.，Highly ornamental。 [8]                        
Species index：IN985654
""")

rag_worker.add_text_to_vector_store("""
Fugui is a succulent herbaceous plant of the Crassulaceae family.。The living blades are short and stick-like，The leaves are gray-green.，Powdered white coating，The leaf margins are edged with purplish-red.，The shape of the leaves varies, with short round shapes, thick square shapes, and other different leaf shapes. [5]Blooming period: summer and autumn。 [6]
The succulent originates from southwestern Africa, Namibia，Cultivated in many places around the world today。Sexually prefer a cool, well-ventilated, and sunny environment，Preferably well-lit.，Likes fat.，Optimal growth temperature is 15-25°C，Winter temperatures do not drop below 5°C.，During the growth period, it needs to be dry and wet.。 [7]It grows well in well-ventilated, well-drained soil.，Generally, a mixture of peat, vermiculite, and perlite can be used.。The propagation method is generally cuttings，Use more branch cuttings.，The success rate of propagation through leaf cuttings is not high.。 [8]
Because the leaf shape and color of the fortune daughter are more beautiful，Therefore has certain aesthetic value，Can be potted and placed next to the TV or computer，Absorbing radiation，It can also be planted indoors to absorb formaldehyde and other substances，Purify the air。 [9]
Species index：IN772
""")

rag_worker.add_text_to_vector_store("""
Stone lotus（ Sinocrassula indica (Decne.) A. Berger）Is the Crassulaceae family of stone lotus [8]Biennial herbaceous plants。Basal leaf rosette，Spoon-shaped and elongated; leaves alternate on the stem，Broadly lanceolate or nearly oval; inflorescence conical or nearly umbellate，The sepals are broad and triangular，The petals are red，Needle-shaped or oval-shaped.，Stamens are square; the beak of the capsule is curved; seeds are smooth; flowering period is September; fruiting period is October [9]。The saw-leaved stone lotus is a variety of the stone lotus.，The difference from the original variant is that the upper part of the leaf has gradually pointed serrations。Stems and flowers are hairless，Ye Beimao. [10]。Because the leaves are jagged and angular，Also resembles jade，Hence the name `stone lotus` [11]。
Species index：IN455674
""")

rag_worker.add_text_to_vector_store("""
Rainbow jade brocade（Sedum × rubrotinctum 'Aurora'） [1]It is a succulent plant of the Crassulaceae family，For the variegated variety of Rainbow Jade。There is no significant change in the size of the leaves of the Rainbow Jade and Rainbow Jade varieties，But the colors may be slightly different，Rainbow satin typically comes in colors like pink and medium green. [2]。Grows much slower than the rainbow jade. [3]。
Species index：IN88
""")

rag_worker.add_text_to_vector_store("""
A specter，The ghost of communism.，Wandering in Europe.。To carry out a sacred encirclement against this specter，All forces of old Europe，The Pope and the Tsar, Metternich and Kossuth, the radicals in France and the police in Germany.，All have united。

Which opposition party is not labeled as a communist by its ruling enemies?？Which opposition party does not use the label of communism to counter more progressive opponents and their own reactionary enemies?？

Two conclusions can be drawn from this fact：

Communism has been recognized by all forces in Europe as a power;

Now is the time for communists to publicly explain their views, their goals, their intentions to the world and to use the party`s own manifesto to refute the myths about the specter of communism。

For this purpose.，Communists from various countries gather in London，Drafted the following declaration.，Published in English, French, German, Italian, Flemish, and Danish.。

1. The bourgeoisie and the proletariat

To this day, the history of all societies is the history of class struggles。

Freemen and slaves, nobles and commoners, lords and serfs, guild masters and apprentices.，In a word，Oppressors and the oppressed.，Always in a position of mutual opposition，Engaging in continuous struggles, sometimes covertly and sometimes openly，And the outcome of each struggle is either a revolutionary transformation of society or the mutual destruction of the contending classes。

In all past historical eras，We can almost see society completely divided into different ranks everywhere.，Seeing social status divided into various levels.。In ancient Rome.，There are nobles, knights, commoners, and slaves，In the Middle Ages.，There are feudal lords, servants, guild masters, helpers, and serfs.，And there are almost some special strata within each class。

The modern bourgeois society that emerged from the demise of feudal society did not eliminate class antagonism.。It merely replaces the old with new classes, new conditions of oppression, and new forms of struggle.。

But.，Our era.，The era of the bourgeoisie.，But it has a characteristic.：It has simplified class antagonism.。The whole society is increasingly divided into two major opposing camps.，Divided into two directly opposing classes：The bourgeoisie and the proletariat.。

The early urban bourgeoisie emerged from the serfs of the Middle Ages; from this citizen class developed the initial bourgeois elements.。

The discovery of America, the navigation around Africa，Opened up a new world for the emerging bourgeoisie。The markets of East India and China, the colonization of the Americas, trade with the colonies, means of exchange, and the increase of general commodities，Causing commerce, shipping, and industry to flourish unprecedentedly，Thus, the revolutionary factors within the collapsing feudal society rapidly developed.。

The previous feudal or guild industrial management methods can no longer meet the increasing demands arising from new markets.。Workshop handcraft replaced this mode of operation。Guild masters have been pushed out by the intermediate levels of industry; the division of labor between various industry organizations has disappeared with the emergence of internal divisions of labor in each workshop。

But.，The market is always expanding.，Demand is always increasing.。Even handicrafts in factories can no longer meet the needs。Then，Steam and machines have caused a revolution in industrial production。Modern large-scale industry has replaced workshop handicrafts; millionaires in industry.，The leader of a battalion of industrial troops，modern capitalists，Replaced the middle class of industry。

Large-scale industry established a world market prepared by the discoveries of America。The world market has greatly developed commerce, navigation, and land transportation.。This development in turn promotes the expansion of industry。At the same time.，With the expansion of industry, commerce, shipping, and railways，The bourgeoisie has developed to the same extent.，Increase their own capital，Push all classes left over from the Middle Ages to the back.。

It can be seen that.，The modern bourgeoisie itself is a product of a long developmental process，Is a product of a series of changes in the modes of production and exchange.。

Every stage of this development of the bourgeoisie，All accompanied by corresponding political progress。It is an oppressed class under feudal lord rule，In the commune, they are armed and self-governing groups，Form independent city-states in some places，In other places, forming the taxed third estate in monarchies; later.，During the period of workshop handicrafts，It is a force that counters the nobility in hierarchical monarchies or despotic states，And is the main foundation of the great monarchies; finally，Since the establishment of large-scale industry and the world market，It has gained exclusive political dominance in modern representative states。The modern state power is merely a committee managing the common affairs of the entire bourgeoisie.。

The bourgeoisie has played a very revolutionary role in history。

The bourgeoisie has destroyed all feudal, patriarchal, and idyllic relations in the places where it has already established its rule。It ruthlessly cuts the various feudal ties that bind people to their natural superiors，It reduces relationships between people to nothing but bare self-interest.，Except for the cold and ruthless `cash transaction`，There is no other connection anymore.。It sanctifies the emotional outbursts of religious piety, chivalrous enthusiasm, and petty bourgeois sentimentality.，Drowned in the icy waters of selfish intentions。It transforms human dignity into exchange value，Replaced countless privileges and self-earned freedoms with a heartless freedom of trade.。In summary.，It replaces the exploitation covered by religious and political fantasies with open, shameless, direct, and blatant exploitation。

The bourgeoisie has erased the sacred aura of all professions that were once respected and revered。It turns doctors, lawyers, clergymen, poets, and scholars into hired laborers it pays to employ。

The bourgeoisie has torn away the tender veil covering family relationships.，Turn this relationship into a purely monetary relationship。

The bourgeoisie reveals.，The barbaric use of human labor that was highly praised by reactionaries in the Middle Ages.，Is correspondingly supplemented by extreme laziness。It was the first to prove，What achievements human activities can attain。It created wonders completely different from the Egyptian pyramids, Roman aqueducts, and Gothic cathedrals; it accomplished expeditions entirely different from the great migrations of peoples and the Crusades.。

The bourgeoisie, unless it is about the means of production.，Thus affecting the production relations，Thus continuously revolutionizing all social relations.，Otherwise, it cannot survive。On the contrary.，maintaining the old modes of production unchanged，It was the primary condition for the survival of all past industrial classes.。The continuous transformation of production.，All social conditions are in constant turmoil.，Eternal instability and change，This is where the bourgeois era differs from all past eras.。All fixed, rigid relationships and the corresponding revered concepts and views have been eliminated，All newly formed relationships become outdated before they can be established.。All hierarchies and fixed structures have vanished，All sacred things have been desecrated。People finally have to look at their living conditions and their relationships with a calm perspective.。

The need to continuously expand the market for products，Forcing the bourgeoisie to rush around the globe。It must settle everywhere，Develop everywhere，Establish connections everywhere.。

Bourgeoisie，Due to the expansion of the world market，has made the production and consumption of all countries global。What makes the reactionaries greatly regret is，The bourgeoisie has undermined the national foundation of industry。The old national industries have been destroyed，And are being eliminated every day。They have been pushed out by new industries，The establishment of new industries has become a matter of vital importance for all civilized nations; these industries process，No longer local raw materials，But rather raw materials from extremely distant regions; their products are not only for domestic consumption，And at the same time, it is supplied for consumption around the world.。The old needs satisfied by domestic products.，Replaced by new needs that must be satisfied by products from extremely distant countries and regions.。The past state of local and national self-sufficiency and isolationism，Replaced by the various interactions and interdependencies of different nations.。Material production is such，The production of spirit is the same。The spiritual products of various nations have become public property.。The one-sidedness and limitations of nations are increasingly becoming impossible，Thus, a world literature is formed from the literatures of many nations and localities。

Bourgeoisie，Due to the rapid improvement of all means of production.，Due to the extreme convenience of transportation，Has drawn all nations, even the most barbaric, into civilization。The low prices of its goods，It is the heavy artillery it uses to destroy all barriers and conquer the most stubborn xenophobia of the barbarians。It forces all nations—if they do not want to perish—to adopt the bourgeois mode of production; it forces them to implement what is called civilization in their own territories.，That is, to become capitalists。In a word，It creates a world for itself according to its own appearance。

The bourgeoisie subjugates the countryside to the rule of the city.。It has created vast cities.，Causing the urban population to greatly exceed the rural population，Thus, it has led a large portion of the population to escape the ignorance of rural life.。Just as it subordinates the countryside to the city，It makes uncivilized and semi-civilized countries subordinate to civilized nations.，Makes the farmers` nation subordinate to the bourgeois nation，Make the East subordinate to the West。

The bourgeoisie increasingly eliminates the scattered state of means of production, property, and population。It densifies the population，Concentrating the means of production，concentrating property in the hands of a few。The inevitable result of this is political centralization。Each region is independent, almost only having an alliance relationship, with different interests, laws, governments, and tariffs，Now combined into a unified nation with a unified government, unified law, unified national class interests, and unified tariffs。

The productive forces created by the bourgeoisie in its less than a hundred years of class rule.，More than all the productive forces created by past generations，It must be larger。The conquest of natural forces，The adoption of machines，The application of chemistry in industry and agriculture，The navigation of the ship，The passage of railways，The use of the telegraph.，The cultivation of the entire continent，The navigation of rivers.，As if a large population were summoned from underground by magic.，—Which century in the past could have anticipated such productive forces hidden in social labor?？

It can be seen that.，The means of production and exchange upon which the bourgeoisie is formed，It was created in feudal society.。At a certain stage of the development of these means of production and exchange，The relations of production and exchange in feudal society.，Feudal agriculture and workshop handicraft organization.，In a word，Feudal ownership relations，No longer adapting to the developed productive forces。This relationship has been hindering production rather than promoting it。It has become a shackle that binds production。It must be destroyed，It has already been destroyed。

What replaces it is free competition and the social and political systems that correspond to free competition, the economic and political domination of the bourgeoisie.。

Now，We are witnessing a similar movement before us.。The production and exchange relations of the bourgeoisie，The ownership relations of the bourgeoisie，This modern bourgeois society that once seemed to have magically created such vast means of production and exchange，Now, like a magician, they can no longer control the demons they have summoned with their spells.。The history of industry and commerce over the decades，It is merely the history of modern productive forces resisting modern production relations, resisting the property relations that serve as the conditions for the existence of the bourgeoisie and its rule.。It is enough to point out the commercial crises that increasingly threaten the survival of the entire bourgeois society in periodic repetitions.。During commercial crises，There is always a large portion of manufactured products that are destroyed，And a large part of the productive forces that have already been created has been destroyed。During the crisis，A social plague that seems absurd in all past eras occurs，That is the plague of overproduction。Society suddenly finds itself back in a temporary state of barbarism; as if there were a famine or a widespread catastrophic war.，Has caused society to lose all means of subsistence; as if industry and commerce have been completely destroyed，—What is the reason for this?？Because civilization has become excessive in society，There is an excess of means of livelihood，Industry and commerce are too developed.。The productive forces possessed by society can no longer promote the development of bourgeois civilization and bourgeois property relations; on the contrary.，The productive forces have become so powerful that this relationship can no longer adapt，It has been hindered by this relationship; and as soon as it begins to overcome this obstacle，This plunges the entire bourgeois society into chaos，It threatens the existence of bourgeois ownership。The relationships of the bourgeoisie have become too narrow，It can no longer accommodate the wealth it itself has created。— How does the bourgeoisie overcome this crisis?？On one hand, must eliminate a large amount of productive forces，On the other hand, seize new markets.，To make more thorough use of the old markets.。What kind of method is this?？This is merely a way for the bourgeoisie to prepare for a more comprehensive and intense crisis.，Merely a way to reduce the means of preventing crises。

The weapons the bourgeoisie used to overthrow the feudal system，Now it is directed at the bourgeoisie themselves。

But.，The bourgeoisie not only forged the weapons that would lead to their own destruction; it also produced the people who would wield these weapons—the modern workers，That is, the proletariat.。

With the development of the bourgeoisie, that is, capital，The proletariat, that is, the modern working class, also develops to the same extent; modern workers can only survive when they find work.，And they can only find work when their labor increases capital.。These workers who have to sell themselves sporadically，Like any other goods，It is also a commodity.，Thus, they are equally affected by all changes in competition and all fluctuations in the market。

Due to the promotion of machines and division of labor，The labor of the proletariat has lost any independent nature.，Thus lost any appeal to workers。Workers have become mere appendages to machines，What is required of him is only extremely simple, monotonous, and easy-to-learn operations。Therefore，Expenses incurred on workers.，Almost limited to the means of living necessary to sustain workers` lives and the continuation of workers` descendants。But.，The price of goods，Thus the price of labor，Is equal to its production costs。Therefore，The more labor makes people feel disgusted.，Wages also become less。Moreover.，The more machines are promoted.，The more detailed the division of labor，The more labor is produced, the greater the increase，This may be due to the extension of working hours.，Or due to the increase in labor required over a certain period，The acceleration of machine operations，And so on.。

Modern industry has transformed the paternalistic master`s small workshop into large factories owned by industrial capitalists。The workers crowded in the factories are organized like soldiers.。They are the ordinary soldiers of the industrial army，Under the close surveillance of soldiers and officers at all levels.。They are not merely slaves of the bourgeoisie and the bourgeois state，They are daily and hourly subjected to the machines, to overseers, and primarily to the enslavement of the capitalists operating the factories themselves.。The more this autocratic system openly declares profit as its ultimate goal，The more it is despicable, hateful, and abominable.。

The less skill and strength required for manual operation，In other words.，The more developed modern industry is.，Male workers are increasingly pushed out by female and child workers。For the working class，The differences in gender and age no longer have any social significance。They are merely tools of labor，It only requires different costs due to differences in age and gender。

When the exploitation of workers by factory owners comes to an end，When the workers receive wages paid in cash.，Immediately, another part of the bourgeoisie—landlords, small shopkeepers, pawnbrokers, etc.—rushes towards them.。

The lower levels of the former middle class，That is, small industrialists, small merchants, and petty usurers.，Artisans and peasants—all these classes have descended into the ranks of the proletariat，Some of them lack sufficient small capital to operate large industries，Cannot withstand competition from larger capitalists; some of their skills have become worthless due to new production methods。The proletariat is thus supplemented from all classes of residents。

The proletariat has gone through various stages of development.。Its struggle against the bourgeoisie began simultaneously with its existence.。

Initially, it was individual workers，Then there are the workers of a certain factory，Then there are the workers of a certain labor sector in a certain place.，To struggle against individual capitalists who directly exploit them。They not only attack the production relations of the bourgeoisie.，And they attack the means of production itself; they destroy those foreign goods that come to compete.，Smash the machines.，Burn down factories.，Striving to restore the lost status of medieval workers.。

At this stage，Workers are scattered across the country and divided by competition。The large-scale mobilization of workers，It is not yet the result of their own union.，But rather the result of the unity of the bourgeoisie.，At that time, the bourgeoisie must and can temporarily mobilize the entire proletariat to achieve its political goals。Therefore，At this stage，The proletariat does not fight against its own enemies，But rather to fight against the enemy of their enemy，That is, fighting against the remnants of autocratic monarchy, landlords, non-industrial capitalists, and petty bourgeoisie。Therefore，The entire historical movement is concentrated in the hands of the bourgeoisie; every victory achieved under these conditions is a victory for the bourgeoisie.。

But.，With the development of industry，The proletariat has not only increased in number，And it combines into a larger collective.，Its power is growing increasingly，It increasingly feels its own power。Machines make the differences in labor increasingly smaller，Causing wages to drop to the same low level almost everywhere，Thus, the interests and living conditions within the proletariat are increasingly converging.。The increasingly intense competition among capitalists and the resulting commercial crises.，Making workers` wages increasingly unstable; the rapid and continuous improvement of machines，The entire living status of workers is becoming increasingly insecure; the conflict between individual workers and individual capitalists increasingly has the nature of a conflict between two classes。Workers begin to form alliances against the capitalists; they unite to defend their wages.。They even established regular organizations.，In order to prepare food for possible resistance.。Some places，The struggle erupts as an uprising。

Workers sometimes also achieve victory，But this victory is only temporary.。The true outcome of their struggle was not a direct success，But rather the increasingly expanding union of workers。This union is developed due to the increasingly advanced means of transportation caused by large industries，This means of transportation connects workers from different places.。As long as there is this connection，It can unite many similar local struggles into a national struggle.，Converges into class struggle。And all class struggles are political struggles。The union that medieval citizens could only achieve after hundreds of years through country paths.，Modern proletarians can achieve this by using the railway in just a few years.。

The proletariat organizes into a class，Thus organizing into a political party，Constantly being undermined by the competition among workers。But.，Such organizations always re-emerge，And it is becoming stronger each time.，Stronger.，More powerful。It exploits the divisions within the bourgeoisie，forces them to legally recognize the individual interests of workers。The British Ten Hours Act is an example。

All conflicts within the old society have, in many ways, facilitated the development of the proletariat。The bourgeoisie is in constant struggle.：Initially opposed to the nobility; later opposed to that part of the bourgeoisie that has conflicts of interest with industrial progress; often opposed to all foreign bourgeoisie.。In all this struggle，The bourgeoisie has to appeal to the proletariat，Demand assistance from the proletariat.，This has drawn the proletariat into political movements.。Then，The bourgeoisie itself has given the proletariat its educational factors, that is, the weapons against itself。

Secondly，We have already seen，The progress of industry throws a whole batch of ruling class members into the proletariat，Or at least threatens their living conditions。They also brought a wealth of educational factors to the proletariat。

Finally，In the period when class struggle approaches a decisive battle，The process of disintegration within the ruling class and the entire old society.，Reaching a very intense and sharp degree，Even causing a small portion of the ruling class to detach from the ruling class and join the revolutionary class，That is, the class that holds the future。Therefore，Just as some nobles in the past shifted to the bourgeoisie，Now there are also some people in the bourgeoisie，Especially a part of the bourgeois thinkers who have elevated their understanding to the theoretical level of recognizing the entire historical movement.，Has shifted to the proletariat`s side。

Among all classes currently opposed to the bourgeoisie，Only the proletariat is the truly revolutionary class。The remaining classes are declining and perishing with the development of large-scale industry，The proletariat, however, is a product of large-scale industry itself.。

Intermediate class，namely small industrialists, small merchants, artisans, and farmers，They struggle against the bourgeoisie.，All to maintain the existence of their intermediate class，To avoid extinction。Therefore，They are not revolutionary，But rather conservative.。Moreover.，They are even reactionary，Because they strive to turn back the wheels of history。If they are said to be revolutionary.，That is in view of their impending transition into the ranks of the proletariat，Thus.，They are not defending their current interests，But to protect their future interests，They leave their original positions.，And stand from the perspective of the proletariat。

The lumpenproletariat is the passive and corrupt part of the lowest layer of the old society.，They have also been swept into the movement by the proletarian revolution in some places，But.，Due to their entire living conditions，They are more willing to be bought off，To engage in reactionary activities。

In the living conditions of the proletariat，The living conditions of the old society have been eliminated。The proletarians have no property; their relationship with their wives and children has nothing in common with the bourgeois family relationship; modern industrial labor，Modern capital oppression，Whether in England or France，Whether in America or Germany，They are all the same.，All make the proletariat lose any sense of nationality。Law, morality, and religion are all seen by them as bourgeois prejudices，All that is hidden behind these prejudices are the interests of the bourgeoisie。

After all past classes have fought for domination.，Always makes the entire society subordinate to the conditions for their wealth，Attempting to consolidate their already acquired living status。The proletariat can only abolish their existing mode of possession，Thus abolishing all existing forms of possession，In order to achieve social productivity。The proletariat has nothing of its own that must be protected，They must destroy everything that protects and guarantees private property until now.。

All past movements were either movements of a minority or for the benefit of a minority。The movement of the proletariat is an independent movement for the interests of the vast majority of people。Proletariat，The lowest strata of today`s society，If the entire upper layer constituting the official society is not blown up，Cannot raise their heads.，Stand tall.。

If we speak in terms of form rather than content，The struggle of the proletariat against the bourgeoisie is primarily a struggle within one country。The proletariat of each country should certainly first overthrow the bourgeoisie of their own country.。

When narrating the most general stages of proletarian development，We have sequentially explored the more or less hidden domestic wars within existing society.，Until this war breaks out as an open revolution，The proletariat overthrows the bourgeoisie with violence and establishes its own rule.。

We have already seen，All societies to date are built on the opposition between the oppressing class and the oppressed class。But.，In order to possibly oppress a class，It must ensure that this class at least has the conditions to barely maintain its slave-like existence。Serfs once struggled under serfdom to attain the status of commune members，Petty bourgeoisie once struggled under the constraints of feudal despotism to attain the status of bourgeoisie。Modern workers, however, are the opposite，They do not rise with the progress of industry，But increasingly fall below the living conditions of this class。Workers become destitute.，Poverty is growing faster than population and wealth。It can be clearly seen from this，The bourgeoisie can no longer be the ruling class of society，Can no longer impose the conditions of their class`s existence as the law governing everything on society.。The bourgeoisie can no longer rule，Because it cannot even guarantee that its own slaves maintain a slave`s life.，Because it has to let its slaves fall to the point where they cannot support it, but instead have to support it.。Society can no longer survive under its rule.，That is to say.，Its existence is no longer compatible with society.。

The fundamental conditions for the survival and rule of the bourgeoisie，It is the accumulation of wealth in private hands，It is the formation and proliferation of capital; the condition of capital is wage labor。Wage labor is entirely based on the competition among workers。The industrial progress that the bourgeoisie inadvertently causes and is powerless to resist，The revolutionary union achieved by workers through association replaced their state of dispersion caused by competition.。Then，With the development of large industry，The very foundation upon which the bourgeoisie relies to produce and possess products has been undermined from beneath their feet.。What it first produces is its own gravediggers。The demise of the bourgeoisie and the victory of the proletariat are equally inevitable。

2. The proletariat and communists.

What is the relationship between communists and all proletarians?？

Communists are not a special party opposed to other workers` parties。

They have no interests different from those of the entire proletariat.。

They do not propose any special principles，Used to shape the movement of the proletariat.。

The difference between communists and other proletarian parties is only.：On one hand.，In the struggles of the proletariat of different nations，Communists emphasize and uphold the common interests of the entire proletariat, regardless of nationality; on the other hand，In all the stages of development experienced in the struggle between the proletariat and the bourgeoisie.，Communists always represent the interests of the entire movement。

Therefore，In practical terms，Communists are the most resolute and consistently driving force within the workers` parties of various countries; in theoretical terms，Where they surpass the rest of the proletarian masses is in their understanding of the conditions, processes, and general outcomes of the proletarian movement。

The recent goal of communists is the same as that of all other proletarian parties.：It shapes the proletariat into a class.，Overthrow the rule of the bourgeoisie.，The proletariat seizes power。

The theoretical principles of communists，It is certainly not based on the ideas or principles invented or discovered by this or that reformer of the world。

These principles are merely a general expression of the real relationships of the existing class struggle and the historical movement before us.。Abolish all previously existing property relations，Is not a characteristic unique to communism。

All property relations have undergone constant historical changes and replacements.。

For example，The French Revolution abolished feudal ownership，Replaced by bourgeois ownership.。

The characteristic of communism is not to abolish general ownership，But rather to abolish bourgeois ownership。

But.，Modern bourgeois private property is the final and complete manifestation of production and ownership based on class opposition and the exploitation of some by others.。

In this sense.，Communists can summarize their theory in one sentence.：Abolish private property.。

Some blame us communists，Saying we abolish property earned by individuals through their own labor，To abolish the property that constitutes the basis of all individual freedom, activity, and independence。

What a property earned through labor, earned by oneself! Are you referring to the kind of petty-bourgeois and small peasant property that existed before the emergence of bourgeois property?？That kind of property does not need to be eliminated by us，The development of industry has already eliminated it.，And it is being eliminated every day.。

Or，You are referring to the private property of the modern bourgeoisie, right?？

But.，Isn`t wage labor.，The labor of the proletariat.，Will it create property for the proletariat?？Something that does not exist。The capital created by this labor.，That is, the property that exploits wage labor，Property that can only proliferate under conditions of continuously generating new wage labor for re-exploitation。Today`s property moves within the opposition between capital and wage labor.。Let`s take a look at these two opposing aspects.。

To be a capitalist，That is to say，He occupies not only a purely individual position in production，And occupies a certain social status。Capital is a collective product，It can only be achieved through the collective activities of many members of society，And ultimately, it can only be achieved through the collective activities of all members of society.，Can move into action。

Therefore，Capital is not a personal power.，But rather a social force.。

Therefore，Transforming capital into public property that belongs to all members of society，This does not mean turning personal property into social property。What changes here is only the social nature of property。It will lose its class nature.。

Now，Let`s take a look at wage labor。

The average price of wage labor is the minimum wage，That is, the amount of living materials necessary for workers to maintain their livelihood。Therefore，What hired workers possess through their own labor，Barely sufficient to sustain his life reproduction.。We do not intend to abolish personal ownership of labor products that are used for direct reproduction of life，This kind of possession does not leave any surplus that allows people to control the labor of others.。What we want to eliminate is only the miserable nature of this possession.，Under this possession.，Workers live only to increase capital.，Can only live when the interests of the ruling class require him to be alive.。

In bourgeois society，Living labor is merely a means of augmenting already accumulated labor。In a communist society.，The accumulated labor is merely a means to expand, enrich, and elevate the lives of workers。

Therefore，In bourgeois society, the past dominates the present，In a communist society, the present dominates the past.。In bourgeois society，Capital has independence and individuality，But the active individuals lack independence and personality.。

But the bourgeoisie claims that the abolition of these relations is the abolition of individuality and freedom! That`s right.。Indeed.，It is precisely to eliminate the individuality, independence, and freedom of the capitalists。

Within the scope of today`s bourgeois production relations，So-called freedom is free trade，Free trade。

But.，Trade disappears，Free trade will also disappear。Statements about free trade，Just like all the other grand words about freedom from our bourgeoisie，Only in relation to unfree trade.，For the enslaved citizens of the Middle Ages，Is meaningful.，And regarding communism`s goal to abolish trade, eliminate bourgeois production relations and the bourgeoisie itself，But it is meaningless。

We must abolish private property，You become alarmed.。But.，In your existing society，Private property has been abolished for nine-tenths of the members; this form of private ownership exists because.，precisely because private property has ceased to exist for nine-tenths of its members。Visible，You blame us，It means we must eliminate the ownership that requires the vast majority of people in society to be propertyless.。

In summary.，You blame us，That is to say, we want to abolish your type of property。Indeed.，We are going to do this。

Labor can no longer be transformed into capital, money, or rent，In a word，When it can no longer become a monopolizable social force，That is to say.，From the moment personal property can no longer become bourgeois property，You say，Individuality has been eliminated。

It can be seen that.，You acknowledge，The individuality you understand，Nothing more than capitalists, bourgeois private owners。Such individuality should indeed be eliminated。

Communism does not deprive anyone of the right to own social products，It only deprives the power to use this possession to enslave the labor of others。

Some people argue that.，The abolition of private property，All activities will come to a halt，The wind of laziness will rise.。

That being said，Bourgeois society should have long since perished due to laziness，Because in this society, laborers do not gain，The winners do not labor。All these concerns，can all be reduced to this tautology：Once there is no capital.，There will no longer be wage labor。

All these accusations against the ways of possessing and producing material products of communism，It is also extended to the possession and production of spiritual products.。Just as the termination of class ownership appears to the capitalists as the termination of production itself，The termination of class education, in their view, equals the termination of all education。

The kind of education that capitalists fear losing，For the vast majority of people, it trains humans to become machines。

But.，Since you measure the proposal to abolish bourgeois private property with your bourgeois concepts of freedom, education, law, etc.，Then please do not argue with us.。Your concepts themselves are products of bourgeois production relations and property relations.，Just as your laws are merely the will of your class sanctified as law.，And the content of this will is determined by the material living conditions of your class。

Your egoistic views lead you to transform your production and ownership relations, which are historically and temporarily contingent in the production process, into eternal natural laws and rational laws，This self-serving concept is shared by you and all the ruling classes that have perished。What you can understand when discussing ancient property，What you can understand when talking about feudal ownership，When it comes to bourgeois ownership, you can no longer understand。

Abolish the family! Even the most extreme radicals express outrage at the communists` shameful intention。

What is the foundation of the modern bourgeois family?？It is built on capital.，Built on private wealth。This type of family only exists in a fully developed form among the bourgeoisie，And the forced solitude and public prostitution of the proletariat are its supplements.。

The families of the capitalists will naturally disappear with the disappearance of this supplement，Both will disappear with the disappearance of capital。

Are you blaming us for wanting to eliminate parental exploitation of children?？We acknowledge this charge.。

But.，You say，We replace family education with social education，It is to eliminate the most intimate relationships among people。

And isn`t your education also determined by society?？Isn`t it also determined by the social relations you are in while educating?？Isn`t it also determined by direct or indirect interference from society through schools and so on?？Communists did not invent the role of society in education; they merely seek to change the nature of that role，To free education from the influence of the ruling class。

The family ties of the proletariat are increasingly destroyed by the development of large industry，Their children are increasingly turned into mere commodities and tools of labor due to this development.，The bourgeoisie`s empty talk about family and education, about the intimate relationships between parents and children, is increasingly nauseating.。

But.，You communists are going to implement communal marriage，—— The entire bourgeoisie shouted at us in unison。

Capitalists view their wives merely as production tools。They heard that the means of production will be used publicly，Naturally, one cannot help but think that women will also suffer the same fate。

They never even thought，The issue is to free women from being mere instruments of production.。

In fact，Our capitalists pretend to be virtuous，Expressing surprise at the formal communal marriage system of the so-called communists.，That is nothing short of ridiculous.。The system of public wives does not require communists to implement.，It has almost always existed.。

Our capitalists are not satisfied with having the wives and daughters of their proletarians under their control.，Formal prostitution goes without saying，They also take mutual seduction of each other`s wives as their greatest pleasure.。

The marriage of the bourgeoisie is essentially a form of communal wife system.。People can at most blame the communists，Claiming they want to replace the hypocritically concealed communal marriage with a formal, public communal marriage。In fact，It goes without saying，With the elimination of the current production relations，The communal wife system arising from this relationship，That is, formal and informal prostitution.，Has also disappeared.。

Some even blame the communists，Saying they want to abolish the homeland，Abolish nations。

Workers have no country。Must not deprive them of what they do not have.。Because the proletariat must first achieve political power.，Rising to become a national class.，They organize themselves into a nation，So it is still national in itself，although it is completely different from what the bourgeoisie understands。

With the development of the bourgeoisie，With the realization of trade freedom and the establishment of the world market，With the alignment of industrial production and the corresponding living conditions，The national divisions and oppositions between peoples of different countries are increasingly disappearing.。

The rule of the proletariat will make them disappear more quickly。Collective action，At least a united action of all civilized nations，Is one of the primary conditions for the liberation of the proletariat。

The exploitation of man by man is abolished.，Exploitation of one nation by another will consequently disappear。

Once the class antagonism within the nation disappears.，The antagonistic relations between nations will then disappear。

Various criticisms of communism from religious, philosophical, and all ideological perspectives.，Are not worth discussing in detail。

People`s ideas, viewpoints, and concepts，In a word，People`s consciousness.，Change with the changes in people`s living conditions, social relations, and social existence，Does this require deep thought to understand?？

The history of thought not only proves that spiritual production is transformed along with the transformation of material production.，What else does it prove?？The ruling ideology of any era is always merely the ideology of the ruling class。

When people talk about the idea of revolutionizing the entire society，They merely indicate a fact：Factors of a new society have already formed within the old society.，The disintegration of old ideas is in step with the disintegration of old living conditions。

When the ancient world is heading towards extinction，Various ancient religions were defeated by Christianity.。When Christian thought was defeated by Enlightenment thought in the 18th century.，Feudal society is engaged in a life-and-death struggle with the revolutionary bourgeoisie of the time.。The ideas of freedom of belief and religious freedom.，It only indicates that competition dominates the realm of belief。

`But`，Some may say.，The concepts of religion, morality, philosophy, politics, law, etc., certainly change continuously in the process of historical development，While religion, morality, philosophy, politics, and law have always preserved themselves in this change。

In addition，There still exists an eternal truth common to all social conditions，Such as freedom, justice, and so on。But communism aims to abolish eternal truths，It aims to abolish religion and morality，And not to innovate.，Thus communism contradicts the entire historical development to date。”

What does this criticism boil down to?？The history of all societies to date has been a movement in class opposition.，And this opposition takes different forms in different eras。

But.，Regardless of the forms of class opposition.，The exploitation of one part of society by another has been a common fact throughout the centuries.。Therefore，Not surprising at all，Social consciousness of various centuries，Despite the various forms and differences.，Always moving in certain common forms.，These forms，These forms of consciousness.，It will only completely disappear when class antagonism has completely vanished.。

The communist revolution is the most thorough break with traditional property relations; it is not surprising.，It must achieve a complete break with traditional concepts in its development process。

However.，Let us set aside the various accusations of the bourgeoisie against communism.。

We have already seen earlier，The first step of the workers` revolution is to elevate the proletariat to the ruling class，Strive for democracy。

The proletariat will utilize its political power，Step by step, seize all the capital of the bourgeoisie.，concentrating all means of production in the hands of the state, which is organized as the ruling class of the proletariat，And to increase the total amount of productivity as quickly as possible。

To achieve this，Of course, there must first be compulsory interference with ownership and bourgeois production relations.，That is to take such measures，These measures seem insufficient and powerless economically.，But in the course of the movement, they will exceed themselves，And it is indispensable as a means of transforming all modes of production。

These measures will certainly differ in different countries。

But.，The most advanced countries can almost adopt the following measures：

1. Expropriate land.，Use land rent for state expenditures.。

2. Levying high progressive taxes。

3. Abolish inheritance rights。

4. Confiscate all property of exiles and rebels。

5. By owning state capital and monopolizing the state bank，Concentrate credit in the hands of the state。

6. Centralize all transportation industries in the hands of the state.。

7. Increase state factories and production tools according to the overall plan.，Reclaiming wasteland and improving soil。

8. Implement universal labor obligation system，Establish an industrial army，Especially in agriculture。

9. Combine agriculture and industry，Promoting the gradual elimination of urban-rural opposition。

10. Implement public and free education for all children。Abolish the current form of child labor in factories.。Combine education with material production.，And so on.。

When class differences have disappeared in the process of development and all production is concentrated in the hands of united individuals，Public power loses its political nature.。Political power in its original sense，Is organized violence used by one class to oppress another class。If the proletariat must unite as a class in the struggle against the bourgeoisie，If it becomes the ruling class through revolution，And with the qualification of the ruling class, violently eliminate the old production relations，Then it simultaneously eliminates this production relationship，And thus eliminates the conditions for class opposition，Abolish the very conditions for the existence of classes，Thus eliminating the rule of its own class。

Replacing the old bourgeois society where classes and class antagonisms exist.，It will be such a union，There，The free development of each is the condition for the free development of all.。

III. Literature of Socialism and Communism

1. Reactionary socialism

（A.）Feudal socialism

The nobility of France and England，According to the mission imposed by their historical status，It is to write some works that criticize modern bourgeois society.。During the July Revolution of 1830 in France and the reform movement in England.，They were once again defeated by the detestable upstarts。From then on, serious political struggles could no longer be discussed.。All they can engage in is a struggle of words.。But.，Even in terms of language, it is impossible to replay the old tunes of the restoration period.。In order to arouse sympathy，The nobles had to put on a show，It seems they no longer care about their own interests，Only to write accusations against the bourgeoisie for the benefit of the exploited working class.。The means they use to vent their anger are.：singing songs cursing their new rulers，And muttered some more or less ominous prophecies to him.。

This has produced feudal socialism，Half is a dirge，Half slanderous writing，Half is an echo of the past，Half a threat of the future; sometimes it can also pierce the heart of the bourgeoisie with sharp, witty, and incisive comments，But it is always laughable because it completely fails to understand the process of modern history。

In order to win over the people，The nobility wave the proletariat`s begging bag as a flag。But.，Whenever the people follow them，All find that their backs bear the old feudal emblem，And then laughed out loud，Scattered in a rush.。

A part of the French orthodox and `Young England`，Have all played this role.。

The feudal lord says，Their mode of exploitation is different from that of the bourgeoisie，Then they simply forgot，They exploit under completely different and now outdated circumstances and conditions。They say.，The modern proletariat did not emerge under their rule，Then they simply forgot，The modern bourgeoisie is the inevitable product of their social system.。

However.，They do not hide the reactionary nature of their criticism.，Their main accusation against the bourgeoisie is that：Under the rule of the bourgeoisie, a class is developing that will blow up the entire old social system.。

They blame the bourgeoisie.，Rather than because it produced the proletariat，Rather, it is because it produced a revolutionary proletariat。

Therefore，In political practice，They participate in all violent measures taken against the working class.，In daily life，They contradict their own grandiloquent words，Deigning to pick up golden apples.，Doing business in wool, beets, and distilling without regard for integrity, kindness, and reputation.。

Just as monks always walk hand in hand with feudal lords，Monastic socialism always walks hand in hand with feudal socialism。

To paint Christian asceticism with a layer of socialist color.，It couldn`t be easier.。Isn`t Christianity also fiercely opposed to private property?，Opposing marriage，Oppose the state?？Isn`t it advocating to replace all this with doing good, begging, celibacy, asceticism, monasticism, and worship?？Christian socialism.，It was merely the holy water used by monks to sanctify the grievances of the nobility。

（B）Petty-bourgeois socialism

The feudal nobility is not the only class that has been overthrown by the bourgeoisie; its living conditions have increasingly deteriorated and disappeared in modern bourgeois society.。The medieval town burghers and small peasant class are the predecessors of the modern bourgeoisie。In countries where industry and commerce are not very developed.，This class is barely surviving alongside the emerging bourgeoisie.。

In countries where modern civilization has developed，A new petty bourgeoisie has formed.，It swings between the proletariat and the bourgeoisie，And they are constantly reconstituted as a supplementary part of bourgeois society。But.，Members of this class are often thrown into the ranks of the proletariat by competition，Moreover，With the development of large industry，They even realize that.，They will soon completely lose their status as an independent part of modern society.，In commerce, industry, and agriculture, it will soon be replaced by foremen and employees。

In countries where the peasant class far exceeds half of the population.，For example, in France.，Those authors who stand on the side of the proletariat against the bourgeoisie.，Naturally, it criticizes the bourgeois system using the standards of the petty bourgeoisie and small farmers，Speaks for the workers from the standpoint of the petty bourgeoisie。This formed the socialism of the petty bourgeoisie.。Sismondi is the leader of such authors not only for France but also for Britain。

This socialism analyzes the contradictions in modern production relations very thoroughly.。It exposes the hypocritical embellishments of economists。It conclusively proves the destructive effects of machinery and division of labor, the accumulation of capital and land, overproduction, crises, the inevitable decline of small capitalists and small farmers, the poverty of the proletariat, the anarchic state of production, the extremely uneven distribution of wealth, and the destructive industrial wars between nations.，The disintegration of old customs, old family relationships, and old national identities。

But.，This socialism, in terms of its actual content,，Or attempting to restore old means of production and exchange，Thus restoring the old property relations and the old society，Or attempting to forcibly shove modern means of production and exchange back into the outdated ownership relations that have already been transcended and will inevitably be transcended。It is reactionary in both cases，At the same time, it is also utopian。

The guild system in industry.，Patriarchal economy in agriculture，——This is its conclusion。

This ideology later developed into a timid lament.。

（C.）German or `real` socialism.

The literature of socialism and communism in France arose under the oppression of the ruling bourgeoisie，And it is a written expression of the struggle against this domination.，When this literature was moved to Germany，There, the bourgeoisie has just begun to fight against feudal despotism。

German philosophers, semi-philosophers, and literary figures.，Greedily seized this literature，However, they have forgotten.：When this kind of work moved from France to Germany，The living conditions in France did not move over at the same time。Under the conditions in Germany.，French literature has completely lost its direct practical significance，But only has the form of pure literature。It inevitably manifests as futile speculation about the true society and the realization of human essence。Thus.，The demands of the First French Revolution，In the view of 18th-century German philosophers.，It is merely a general requirement of `practical reason`，and the expression of the will of the revolutionary French bourgeoisie，In their minds, it is the law of pure will, original will, and the will of true humanity.。

The sole work of German authors，It is to reconcile the new French thought with their old philosophical beliefs.，Or rather，It is to grasp French thought from their philosophical perspective。

This mastery，Just like mastering a foreign language，It is through translation。

Everyone knows，Monks once wrote absurd Catholic saint biographies on manuscripts of ancient pagan classics.。German authors take the opposite approach to secular French literature。They write their philosophical nonsense under the original works in France。For example，They wrote `the externalization of human essence` under the French critique of monetary relations，Under the French critique of the bourgeois state, write the so-called `abolition of the rule of abstract universal commodities`，And so on.。

This practice of inserting one`s philosophical phrases into the discourse of the French，They call it `philosophy of action`, `true socialism`, `German socialist science`, `philosophical argument for socialism`.，And so on.。

The literature of socialism and communism in France has thus been completely emasculated。Since this kind of literature no longer represents the struggle of one class against another in the hands of Germans，Thus, the Germans believe：They have overcome the `one-sidedness of the French`，They do not represent real demands.，And the demands that represent the truth，Does not represent the interests of the proletariat，And represent the essential interests of people.，That is, the interests of the general public，Such people do not belong to any class，Does not exist at all in the real world.，And only exists in the space of philosophical fantasies shrouded in mist。

This German socialism, which once took its own set of poor student assignments seriously and shamelessly boasted about them.，Has gradually lost its naive self-congratulatory erudition。

The struggle of the bourgeoisie in Germany, especially Prussia, against feudal lords and autocratic dynasties，In a word，Liberal movement，It is becoming increasingly serious。

Then，The `real` socialism has gotten a good opportunity，Opposing the demands of socialism to political movements，Cursing liberalism in the traditional way of cursing heretical doctrines，Cursing representative states，Cursing the competition of the bourgeoisie, the freedom of the bourgeois press, the law of the bourgeoisie, the freedom and equality of the bourgeoisie，And they widely promote to the masses.，Saying that in this bourgeois movement，The masses of people gain nothing.，The more it will lose everything。German socialism has just forgotten，Critique of France（German socialism is a pathetic echo of this critique）It is based on modern bourgeois society and corresponding material living conditions and political systems，And all these premises were yet to be fought for in Germany at that time。

This type of socialism has become a straw man for the autocratic governments of the German states and their followers—clergymen, educators, Junkers, and bureaucrats—who seek to intimidate the bourgeoisie.。

This socialism is the sweet complement of the vicious whip and bullets used by these governments to suppress the German workers` uprising。

Since `true` socialism has thus become a weapon for these governments against the German bourgeoisie，Then it directly represents a reactionary interest.，That is, the interests of the German petty bourgeoisie。In Germany，The petty bourgeoisie left over from the 16th century, which has frequently reappeared in different forms since then，Is the real social foundation of the existing system。

Preserve this petty bourgeoisie，It is to preserve the existing system of Germany。This class anxiously awaits its inevitable demise from the industrial and political rule of the bourgeoisie，This is partly due to the accumulation of capital，On the other hand, it is due to the rise of the revolutionary proletariat。In its view.，`True` socialism can serve a dual purpose。`True` socialism has spread like a plague。

German socialists drape their few dry `eternal truths` in a garment woven from the threads of speculative thought, adorned with flowery language and soaked in sweet sentiment，This splendid exterior only serves to increase the market for their goods among these customers.。

At the same time.，German socialism is increasingly recognizing its mission to act as a spokesperson for the petty bourgeoisie`s grandiloquent talk.。

It declares the German nation to be a model nation.，The German petty bourgeois is the model person.。It adds a mysterious, noble, and socialist meaning to every vice of these petty bourgeois.，Transforming it into something completely opposite。It develops to the end，Directly opposing the `savage destruction` tendency of communism，And declare themselves to be above any class struggle in an impartial manner。All so-called socialist and communist writings currently popular in Germany.，With very few exceptions，All belong to this kind of despicable, sordid, and demoralizing literature。

2. Conservative or bourgeois socialism.

Some people in the bourgeoisie want to eliminate the ills of society，In order to ensure the survival of bourgeois society.。

This part of the people includes：Economists, philanthropists, humanitarians, advocates for the improvement of the working class`s conditions, charity organizers, animal protection association members, temperance movement initiators, and various minor reformers。This bourgeois socialism has even been formed into some complete systems。

We can take Proudhon`s `The Philosophy of Poverty` as an example。

Socialist capitalists are willing to accept the conditions for survival in modern society，But do not let the struggles and dangers that necessarily arise from these conditions.。They are willing to accept the existing society，But do not want those factors that revolutionize and dissolve this society。They are willing to have the bourgeoisie，But do not want the proletariat.。In the eyes of the bourgeoisie，The world it dominates is naturally the best world。The bourgeois socialism has turned this comforting idea into a half or full set of systems。It requires the proletariat to realize its system，Walking into the New Jerusalem，In fact, it merely demands that the proletariat remain in the current society.，But must abandon their abhorrent views about this society。

Another form of socialism that is not systematic enough but more practical，Striving to make the working class disdain all revolutionary movements，It is not this or that political reform that can supposedly benefit the working class，But merely a change in material living conditions, that is, economic relations。But.，The changes in material living conditions understood by this socialism.，The abolition of bourgeois production relations is not achievable solely through revolutionary means，But rather some administrative reforms implemented on the basis of these production relations，Thus will not change the relationship between capital and wage labor in the slightest，At most, it can only reduce the ruling costs of the bourgeoisie and simplify its financial management.。

Bourgeois socialism only exists when it becomes pure rhetoric，Only then does it gain its appropriate expression.。

Free trade! For the benefit of the working class; protective tariffs! For the benefit of the working class; solitary confinement! For the benefit of the working class。— This is the only serious last word of the bourgeois socialism。

The socialism of the bourgeoisie is such a proposition：The essence of capitalists as capitalists，It is for the benefit of the working class.。

3. Critique of Utopian Socialism and Communism

Here，We do not talk about the literature that has expressed the demands of the proletariat in all modern revolutions（The works of Babeuf and others）。

The proletariat`s initial attempt to directly realize its class interests during a time of general agitation and in the period of overthrowing feudal society，All inevitably faced failure，This is because the proletariat itself was not sufficiently developed at that time.，Due to the material conditions for the liberation of the proletariat not yet being in place.，These conditions are merely products of the bourgeois era。Revolutionary literature that emerged alongside these early proletarian movements，In terms of its content, it is inevitably reactionary。This kind of literature advocates for universal asceticism and crude egalitarianism。

The system of socialism and communism in its original sense，The systems of Saint-Simon, Fourier, Owen, and others，It appeared in the early stages when the struggle between the proletariat and the bourgeoisie was not yet developed。Regarding this period.，We have already described this earlier.（See `The Bourgeoisie and the Proletariat`）。

Indeed.，The inventors of these systems saw the class antagonism.，As well as the role of disintegrating factors within the dominant society itself。But.，They see no historical initiative from the proletariat，Cannot see any political movement unique to it。

The development of class opposition is in step with the development of industry.，Therefore, these inventors cannot foresee the material conditions for the liberation of the proletariat，Thus, they seek some kind of social science, social laws.，In order to create these conditions.。

Social activities should be replaced by their individual inventive activities，The historical conditions for liberation must be replaced by imaginary conditions，The gradual organization of the proletariat into a class must be replaced by a specially designed social organization.。In their view，The future world history is nothing but the promotion and implementation of their social plans.。

Indeed.，They also realize，Their plans mainly represent the interests of the working class, the most suffering class.。In their minds.，The proletariat is merely the class that suffers the most.。

But.，Due to the lack of development in class struggle，Due to their own living conditions.，They think they are above this class opposition.。They aim to improve the living conditions of all members of society，Even the most affluent members are included.。Therefore，They always indiscriminately appeal to the entire society，And it mainly appeals to the ruling class。They thought，People just need to understand their system，Will acknowledge this system as the best plan for the best society。

Therefore，They reject all political action，Especially all revolutionary actions; they want to achieve their goals through peaceful means.，And they attempt to conduct some small-scale, of course unsuccessful experiments.，To pave the way for a new social gospel through the power of demonstration.。

This depiction of fantasies about future society，When the proletariat is still underdeveloped, and thus their understanding of their own position is still based on illusions，It corresponds to the initial instinctive desire of the proletariat for the universal transformation of society.。

But.，These works of socialism and communism also contain critical elements。These works criticize the entire foundation of the existing society.。Therefore，They provide extremely valuable material for enlightening workers` consciousness.。Their positive propositions about future society.，For example, the elimination of the urban-rural divide.，Abolition of the family.，Abolish private profit，Abolish wage labor.，Advocating social harmony.，Transform the state into a purely production management institution，— All these claims merely indicate the need to eliminate class opposition.，And this class opposition was just beginning to develop at that time，What they know is only the early, indistinct, and uncertain forms of this opposition.。Therefore，These claims themselves still carry a purely utopian nature。

The significance of critical utopian socialism and communism，Is inversely proportional to the development of history。As class struggle develops and takes on more definite forms.，This fantasy beyond class struggle，This fantasy against class struggle.，The more it loses any practical significance and any theoretical basis。Therefore，Although the founders of these systems are revolutionary in many respects.，But their followers always form some reactionary sects.。These believers ignore the historical progress of the proletariat.，Or stubbornly cling to the old views of their teachers。Therefore，They consistently attempt to weaken class struggle，Harmonizing contradictions.。They always dream of realizing their social utopia through experimental methods.，Establishing a single Falun Steel，Establish domestic immigrant zones.，Establishing a small Utopia.，A pocket-sized new Jerusalem，——And in order to build all these castles in the air，They had to appeal to the bourgeoisie for kindness and generosity。They gradually fell into the aforementioned reactionary or conservative socialists` group，The difference is that they flaunt their knowledge more systematically.，Fanatically superstitious about the miraculous effects of their own social sciences。

Therefore，They fiercely oppose all political movements of the workers，Believing that this movement occurred solely due to a blind disbelief in the new gospel.。

In England，There are Owenites opposing the Charterists，In France.，There are Fourierists opposing the reformists.。

4. The attitude of communists towards various opposing parties

After reading the second chapter.，One can understand the relationship between communists and the already formed workers` parties，Thus, they can also understand their relationship with the British Chartists and the North American land reformers.。

Communists fight for the immediate aims and interests of the working class，But they simultaneously represent the future of the movement in the current struggle.。In France.，Communists unite with the socialist democrats to oppose the conservative and radical bourgeoisie，But this does not give up the right to take a critical attitude towards the empty talk and fantasies inherited from revolutionary traditions。

In Switzerland，Communists support the radicals，However, it should not be overlooked that this party is composed of contradictory elements.，Some of them are French-style democratic socialists.，A part of them are radical capitalists。

Among the Poles，Communists support the party that regards land reform as a condition for national liberation，The party that instigated the Kraków uprising of 1846。

In Germany，As long as the bourgeoisie takes revolutionary action，The Communist Party opposes autocratic monarchy, feudal land ownership, and the reactionary nature of the petty bourgeoisie.。

But.，The Communist Party does not neglect to educate workers to be as clear as possible about the antagonistic opposition between the bourgeoisie and the proletariat.，So that German workers can immediately use the social and political conditions inevitably brought about by bourgeois rule as weapons against the bourgeoisie，So as to immediately begin the struggle against the bourgeoisie itself after overthrowing the reactionary class in Germany。

Communists focus their main attention on Germany.，Because Germany is on the eve of the bourgeois revolution，Because compared to 17th century England and 18th century France，Germany will be under more progressive conditions of European civilization，The proletariat, which has developed much more, will realize this transformation，Thus, the bourgeois revolution in Germany can only be a direct prelude to the proletarian revolution.。

In summary，Communists everywhere support all revolutionary movements against the existing social and political systems。

In all these movements，They all emphasize that the issue of ownership is the fundamental issue of the movement.，Regardless of the level of development of this issue。

Finally，Communists everywhere strive for unity and coordination among democratic parties worldwide。

Communists disdain to conceal their views and intentions。They openly declare：Their goal can only be achieved by violently overthrowing all existing social systems。Let the ruling class tremble before the communist revolution。The proletariat loses only its chains in this revolution。What they gain will be the whole world。

Proletarians of the world，Unite!
""")

query = 'Species of the blessed mother.'
nodes = rag_worker.retrieve_from_store_with_query(query)
build_prompt = rag_worker.build_prompt(query, nodes)
preview = rag_worker.generate_node_array_preview(nodes)
print(preview)
print(build_prompt)
print(nodes)

# vs = rag_worker.load_from_checkpoint('./good_man_vector_store')
# rag_worker.add_text_to_vector_store(r"I see that the (0.6.0) index persisted on disk contains: docstore.json, index_store.json and vector_store.json, but they don't seem to contain file paths or title metadata from the original documents, so maybe that's not captured and stored?")
# rag_worker.add_text_to_vector_store(r"Thanks! I'm trying to cluster (all) the vectors, then generate a description (label) for each cluster by sending (just) the vectors in each cluster to GPT to summarize, then associate the vectors with the original documents and classify each document by applying a sort of weighted sum of its cluster-labeled snippets. Not sure how useful that will be, but I want to try! I've got the vectors now (although I'm bit worried that the nested structure I'm getting them from might change without warning in the future!), and I'm able to cluster them, but I don't know how to associate the vectors (via their nodes) back to the original documents yet...")
# res = rag_worker.retrieve_from_store_with_query('cluster')
# rag_worker.save_to_checkpoint(checkpoint_dir = './good_man_vector_store')

# print(vs)
