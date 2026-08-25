# ABCW Paper — Master Draft v0.4

> Integrated master draft with Sec. 1–9, main-paper Figures 1–6, and Tables 1–4. v0.4 incorporates minor-review revisions for reproducibility and figure-text linkage: the simulation learning rate and exact non-baseline initial-field edge sets are specified, and explicit callouts are added for the global sign-flip symmetry, exact lower-bound decomposition, and internal 692-class structure. No experimental result or numerical claim is changed.

---

# 1. Introduction

複雑な力学系を記述するとき、現在の状態を細かく知るほど未来を正確に予測できるとは限らない。完全なミクロ状態は未来を決定するために十分であるとしても、そのすべての区別が、特定の予測目的に対して必要であるとは限らない。

本研究が扱う中心的な問いは、次のように表せる。

> **未来を予測するために、現在のどの区別を残す必要があるか。**

より直感的には、

> **未来を知るために、現在をどこまで忘れてよいか。**

という問いである。

この問題は、状態空間の粗視化や状態集約、Markov chainにおけるlumpability、bisimulationによるmodel minimization、computational mechanicsにおけるcausal states、さらにincompletely specified finite-state machineの状態最小化など、複数の既存研究と関係する。

これらの研究には、ミクロ状態のすべての区別を保持するのではなく、将来の力学や予測目的に必要な区別を保存しながら状態表現を縮約するという共通した問題意識がある。一方、それぞれが保存しようとする対象と、縮約後の表現に要求する性質は異なる。

本研究は、これらの一般理論そのものを新たに提案するものではない。本稿では、有限かつ明示的に計算可能なエージェントベース力学を対象として、指定された一時刻先予測を完全に保存するために必要な状態の区別を具体的に求める。

その対象として、本研究では5主体のABCWモデルを用いる。各主体は二値の行動と戦略を持ち、主体間の影響関係は時間変化する重み行列 $${W}$$ によって表される。主体の行動は局所的な影響関係を参照して更新され、ゲームの勝敗は戦略および場の更新へフィードバックされる。

競合的な利得構造にはMinority Game型の規則を用いる。ただし、ABCWは標準的なMinority Gameそのものを再現することを目的とするモデルではない。本稿ではこの規則を、主体間に「全員が同時には勝てない」という競合性を導入するために用いる。Minority Gameおよびその背景にあるEl Farol型の競合問題との関係については、モデルの位置づけとともに後述する。

したがってABCWは、主体の行動と相互作用場が相互に時間発展する有限エージェント系となる。

本稿では、完全対称な基準場 $${W^\ast}$$ からの偏差

$${\Delta W=W-W^\ast}$$

をfield variableとして扱う。5主体ABCWについて4種類の初期場と、各初期場に対する全行動・全戦略初期条件を用い、合計4,096初期条件から完全状態が再訪するまで時間発展を追跡した。その結果、本稿で解析する有限到達集合として56,536遷移、2,562種類の異なる現在場 $${\Delta W}$$、11,202種類の異なる $${(a,\Delta W)}$$ 状態が得られた。

この有限力学に対し、本研究では観測を、単なる変数選択ではなく、

$${P:\Omega\longrightarrow Y}$$

という写像として扱う。すなわち観測 $${P}$$ は、完全状態のどの違いを残し、どの違いを捨てるかを定める。

ここで重要なのは、観測自身の時間発展が閉じていることと、指定された未来を予測できることを区別することである。

観測 $${P}$$ について、

$${P(X_t)\longrightarrow P(X_{t+1})}$$

が一価であることを要求するself-closureと、指定された予測対象 $${Z}$$ に対して

$${P(X_t)\longrightarrow Z}$$

が一価であることは、同じ条件ではない。

本研究の主要な予測目的は後者である。

具体的には、現在の行動 $${a_t}$$ を保持したうえで、現在場 $${\Delta W_t}$$ をより粗いfield classへ写し、それでも一時刻先の完全な場 $${\Delta W_{t+1}}$$ を一意に決定できるかを問う。

本稿では、場の記述をどこまで圧縮できるかを研究対象とするため、行動 $${a_t}$$ は条件変数としてそのまま保持する。したがって、行動空間自体の圧縮を同時に最適化する問題は扱わない。このfield-onlyという制約は、本稿で解く最小化問題の適用範囲の一部である。

field-only写像

$${B:\Delta W\longrightarrow\mathcal C}$$

を用いて、

$${P_B(X_t)=\bigl(a_t,B(\Delta W_t)\bigr)}$$

とし、

$${\bigl(a_t,B(\Delta W_t)\bigr)\longrightarrow\Delta W_{t+1}}$$

が観測された全遷移上で一価となることを要求する。

本稿では、このように指定された予測対象を曖昧さなく決定できる性質を **predictive sufficiency** と呼ぶ。

この設定のもとで、まずノルム、局所構造、out-strengthなど、人間があらかじめ選んだ自然なネットワーク特徴量による場の圧縮を検討する。これらの特徴量の一部は高い予測性能を示すが、検討した候補集合の範囲では、真に異なる $${\Delta W}$$ を統合しながら一時刻先の完全場を100%予測する特徴量は得られなかった。

しかし、この結果だけから、完全予測には2,562種類の現在場をほぼすべて区別する必要があるとは結論できない。

そこで、特徴量を人間が先に選ぶという制約を外し、

> **未来を取り違えないために、現在場のどの区別を残す必要があるか**

を観測された力学から直接求める。

現在場を $${\Delta W}$$、行動条件を $${a}$$、一時刻先の完全場を $${\Delta W'}$$ とみなせば、今回の有限データは概念的に

$${(\Delta W,a)\longmapsto\Delta W'}$$

という部分指定されたinput-output behaviorとして読むことができる。

同じ行動条件のもとで異なる次場を生成する二つの現在場は、同じfield classへまとめることができない。

そこで本研究では、2,562種類の現在場を頂点とし、

> **ある共通の行動条件のもとで異なる次場を生じる二場の間に辺を張る**

incompatibility graph $${G}$$ を構成する。

このとき、一時刻先完全場の100%予測を保存するfield-only partitionは、$${G}$$ のproper coloringに対応する。

本問題では、得られたfield classを次時刻の内部状態として再帰的に運用することを要求しない。保存対象は縮約されたclass labelではなく、一時刻先の完全場 $${\Delta W_{t+1}}$$ そのものである。

したがって、古典的なincompletely specified finite-state machine minimizationで現れる後続クラスに対するrecursive closureを課す必要はなく、本稿のdepth-1 prediction problemでは、最小field class数を

$${|\operatorname{Im}B_{\min}|=\chi(G)}$$

というgraph-coloring problemとして直接求めることができる。

ここでcompatibilityそのものを同値関係として仮定する必要はない。観測された共通行動条件のもとで同一視できない二場をincompatibility edgeとして直接表現し、proper coloringによってそれらを異なるクラスへ分離する。この定式化と古典的なstate-minimization問題との関係はSec. 2で詳しく整理する。

本稿の主結果は、

$${\chi(G)=692}$$

である。

すなわち、本稿で観測された有限到達集合と一時刻先完全場予測という条件のもとでは、2,562種類の異なる現在場をすべて保持する必要はなく、

$${2562\longrightarrow692}$$

までfield classを圧縮しながら、一時刻先の完全な $${\Delta W}$$ の100%予測を維持できる。



![Figure 1. Predictive-partition problem. Schematic of the central prediction problem. The complete ABCW state is compressed by retaining the action and replacing the full field deviation with a field-only partition label. The prediction target is the exact one-step-ahead field deviation. The main result reduces 2,562 observed fields to a minimum of 692 classes.](figures/Fig1_predictive_partition_problem.png)

*Figure 1. Predictive-partition problem. Schematic of the central prediction problem. The complete ABCW state is compressed by retaining the action and replacing the full field deviation with a field-only partition label. The prediction target is the exact one-step-ahead field deviation. The main result reduces 2,562 observed fields to a minimum of 692 classes.*
field class数に基づく圧縮率は、

$${1-\frac{692}{2562}\simeq72.99\%}$$

である。

ここでいう72.99%はクラス数に基づく圧縮率であり、情報量そのものを72.99%削減したことを意味しない。

さらに、692という値は単なる彩色アルゴリズムの出力ではない。

単一のアンカー行動

$${a=(-,-,-,-,-)}$$

のもとでは、観測された1,239種類の現在場から625種類の異なる次場が生じるため、少なくとも625クラスが必要となる。

しかし、この625群のうち50群では、他の行動条件を考慮すると群内部にさらにincompatibilityが残る。これら50群の誘導部分グラフについて、clique lower boundとcolorability searchを組み合わせてchromatic numberを厳密に求めると、追加で67クラスが必要となり、

$${625+67=692}$$

という下界が得られる。

一方、全2,562場からなるincompatibility graphに対して692色のproper coloringを実際に構成し、そのfield-only observationを元の56,536遷移へ戻して検証すると、すべての観測状態について一時刻先完全場が一意に定まる。

したがって上界と下界が一致し、

$${\chi(G)=692}$$

が厳密に確定する。

この結果が示すのは、692という数そのものが普遍的なマクロ状態数であるということではない。

692は、5主体ABCW、baseline / Hub / Local / Hub+Localという4種類の初期場、そこから得られた有限到達集合、行動 $${a}$$ を観測に保持するfield-only圧縮、および一時刻先の完全場を100%予測するという条件に依存する。

したがって、本稿は「ABCW一般の最小状態数は692である」とは主張しない。

より重要なのは、

$${\text{ミクロに異なること}}$$

と

$${\text{未来予測のために区別する必要があること}}$$

が一致しないという点である。

今回の有限ABCWでは、ミクロには異なる複数の場を同一の予測クラスへまとめても未来を失わない場合がある。実際、2,562種類の場のうち、692クラスへの統合によって一時刻先完全場の100%予測を維持できる。

一方、単純なネットワーク特徴量や場の幾何学的な近さだけでは、どの区別を残す必要があるかを完全には捉えられない。

この意味で、本研究は

$${\text{ミクロな完全記述}}$$

と

$${\text{単純なマクロ統計量}}$$

の間に、

$${\text{指定された未来に対して必要な区別だけを残した状態記述}}$$

という別の記述水準を具体的に構成する。

本研究の主要な貢献は、次の三点にまとめられる。

第一に、有限ABCW力学に対して、self-closureとtarget predictionを区別し、「現在のどの区別を残せば指定された未来を完全に予測できるか」という問題を明示的な観測写像の最小化問題として定式化する。

第二に、人間が事前に選んだネットワーク特徴量による圧縮と、未来応答から逆算される予測分割を区別し、今回のdepth-1 prediction problemをincompatibility graphの彩色問題として構成する。

第三に、今回の有限到達集合について、その最小field class数が692であることを上界構成と独立な下界によって厳密に確定し、2,562種類のミクロな場の区別すべてが一時刻先予測には必要ではないことを示す。

これらの貢献は、state minimization、lumpability、bisimulation、causal statesなどの一般理論そのものの新規性を主張するものではない。本研究の位置づけは、それらと関連する問題を有限ABCW力学上の具体的なdepth-1 prediction problemとして構成し、完全に検査可能な有限データ上で厳密最小値まで求めることにある。

以下、Sec. 2ではlumpability、bisimulation、computational mechanics、およびincompletely specified finite-state machine minimizationとの関係を整理し、本研究の位置づけを明確にする。Minority Game型の競合規則についてはABCWのモデル上の役割を区別して扱う。Sec. 3ではABCWモデルと有限到達データセットを定義する。Sec. 4では観測、self-closure、predictive sufficiency、および本稿で用いる予測目的を定式化する。Sec. 5では自然なネットワーク特徴量による圧縮とその限界を検討する。Sec. 6ではincompatibility graphを用いて一時刻先完全場予測を保存する最小field-only partitionを構成し、その厳密最小値を求める。Sec. 7では692クラスの内部構造を解析し、Sec. 8で結果の意味と既存研究との関係を議論する。Sec. 9で結論を述べる。

---

# 2. Related Work and Positioning

## 2.1 Competitive agent models: El Farol and the Minority Game

ABCWモデルの競合的な利得構造は、El Farol Bar problemおよびMinority Gameと問題意識の一部を共有する。

Arthur (1994) のEl Farol Bar problemでは、複数の主体が同じ限られた資源や機会を利用しようとするとき、各主体にとって望ましい選択が他主体の選択に依存する状況が考察される。参加者が少なければ参加することが有利である一方、多数が同じ選択をすればその選択の価値が低下する。このため、個々の主体にとっての合理的な行動を、他主体から独立して固定することができない。

Challet and Zhang (1997) によるMinority Gameは、この競合構造を単純化した二択ゲームとして定式化する。各時刻に主体が二つの選択肢のいずれかを選び、少数派に属した主体が利得を得る。したがって、ある行動の価値はその行動そのものに固定されているのではなく、他主体がどの行動を選んだかによって決まる。

ABCWでも、このMinority Game型の競合性を利用する。5主体の各主体は二値行動を取り、少数派に属した主体を勝者、多数派を敗者とする。これにより、「全主体が同時に同じ意味で成功する」ことのできない競合的な利得環境を導入する。

ただし、ABCWは標準的なMinority Gameの再現、拡張、あるいはその典型的な集団現象の解析を目的とするものではない。

標準的なMinority Game研究では、主体が利用する戦略、情報履歴、適応、およびそれらから生じる集団的な効率性や変動などが主要な分析対象となる。これに対して本研究で中心となるのは、主体間の影響関係そのものを表す時間変化する場 $${W}$$ である。

ABCWでは、ゲームの勝敗が主体の得点だけでなく場の更新へフィードバックされる。したがって、Minority Game型の競合規則は最終的な研究対象ではなく、

$${\text{行動}\longrightarrow\text{勝敗}\longrightarrow\text{場の更新}\longrightarrow\text{次の行動}}$$

という相互作用を生じさせる構成要素として用いられる。

本稿の主要な問いも、「Minority Gameにおいてどの戦略が優位か」あるいは「集団がどのような効率性を示すか」ではない。

本研究が問うのは、このような競合的エージェント力学によって生成された場の時間発展について、

> **一時刻先の場を完全に予測するために、現在場のどの区別を残す必要があるか**

である。

したがって、El FarolおよびMinority GameはABCWに競合的エージェント力学を導入するモデル上の背景を与える一方、本稿のpredictive state reductionそのものの直接的な理論的基盤ではない。後者については、以下のstate aggregationおよびfinite-state minimizationとの関係がより直接的である。

## 2.2 State aggregation and the question of relevant distinctions

本研究の中心的な問いは、

> **未来を予測するために、現在のどの区別を残す必要があるか**

というものである。

この問いは、状態空間をより小さな表現へ集約しながら、元の力学または予測に必要な性質を保存しようとする既存研究と広く関係する。

代表的な例として、Markov chainにおけるlumpabilityがある。Kemeny and Snell (1960) による古典的な定式化では、状態空間を複数のlumpへ分割したとき、同一lump内のどの状態から出発しても次のlumpへの遷移確率が一致するならば、集約後の過程もMarkov chainとして閉じる。この意味でlumpabilityは、ミクロ状態をまとめた後にもwell-definedな縮約ダイナミクスが存在するための条件を与える。

本研究でSec. 4に導入するself-closure、

$${P(X)=P(X')}$$

ならば

$${P(\Phi(X))=P(\Phi(X'))}$$

という条件は、決定論的な有限力学において、これと近い問題意識を持つ。すなわち、同じ観測状態へまとめられた二つの完全状態が、次時刻にも同じ観測状態へ進むことを要求する。

ここで $${X}$$ は完全状態、$${\Phi}$$ は完全状態上の一時刻更新写像であり、$${P:\Omega\to Y}$$ は完全状態空間上の一般的な観測写像である。後に最小化の対象とするfield-only写像 $${B:\Delta W\to\mathcal C}$$ とは区別する。

ただし、本研究の主要問題はself-closureそのものではない。

本稿では、観測された状態自身の次状態

$${P(X_{t+1})}$$

を予測することと、別に指定された予測対象

$${Z=g(X_{t+1})}$$

を予測することを区別する。

したがって、要求する条件は一般には

$${P(X_t)\longrightarrow P(X_{t+1})}$$

の閉包ではなく、

$${P(X_t)\longrightarrow Z}$$

の一価性である。

この区別が、本研究におけるstate aggregationの出発点となる。

## 2.3 Bisimulation and model minimization

状態を、その将来挙動を保存するようにまとめるという考え方は、bisimulationおよびそれを用いたmodel minimizationとも関係する。

例えばGivan, Dean, and Greig (2003)はMarkov decision processにおける状態同値性を検討し、bisimulationに基づく状態集約によって、縮約されたMDPから元のMDPの最適方策を保存できるモデル最小化を論じている。

この方向の研究と本研究に共通するのは、状態の表面的な類似性ではなく、**将来の振る舞いにとって区別が必要かどうか**によって状態をまとめる点である。

一方、本研究で扱う対象はMDPではない。今回のABCWは、保存された有限到達集合上では決定論的な更新則を持ち、本稿で最小化する対象も完全状態全体ではない。

完全状態を

$${X=(a,s,W)}$$

としたとき、本稿では行動 $${a}$$ を観測に保持し、場

$${\Delta W}$$

だけを写像

$${B:\Delta W\longrightarrow\mathcal C}$$

によって圧縮する。

さらに保存したい対象も、最適方策、報酬、あるいは縮約された力学全体ではなく、一時刻先の完全な場

$${\Delta W_{t+1}}$$

である。

したがって、本研究の最小分割をbisimulation quotientそのものと呼ぶことはしない。

## 2.4 Computational mechanics and causal states

本研究の問題意識にさらに近い考え方として、computational mechanicsにおけるcausal statesがある。

Shalizi and Crutchfield (2001)は、過去を、その過去に条件づけられた未来の確率分布が等しい場合に同一視することでcausal statesを定義する。この表現によって得られるε-machineは、予測に必要な情報を保持する最小表現として特徴づけられる。

ここには本研究と明瞭な共通点がある。

完全な過去またはミクロ状態の違いをそのまま保存するのではなく、

> **未来にとって区別可能かどうか**

によって状態を分類するという発想である。

本研究で得られる692クラスも、静的なネットワーク形状の類似性ではなく、行動条件に対する一時刻先の未来応答を保存するよう構成される。

しかし、両者を同一視することはできない。

causal statesは、原則として過去の履歴を未来系列の条件付き確率分布によって同値類へ分ける。一方、本研究では、有限到達集合上の現在場 $${\Delta W}$$ を対象とし、予測対象を一時刻先の完全場 $${\Delta W_{t+1}}$$ に限定する。

また、本研究のデータは部分指定されている。すべての現在場についてすべての行動条件が観測されているわけではない。そのため、「観測された条件のもとで衝突しない」という関係は、一般には推移的な同値関係になるとは限らない。

したがって、本稿では692クラスをcausal statesあるいはε-machineとは呼ばない。

両者の関係は、

$${\text{future-relevant distinctions}}$$

を残すという問題設定上の類似性として位置づける。

## 2.5 Incompletely specified finite-state machine minimization

本研究の最小分割問題と、より直接的な数学的対応を持つのは、incompletely specified finite-state machineの状態最小化である。

この問題の古典的研究としてPaull and Unger (1959)がある。incompletely specified machineでは、すべてのstate-input pairについて出力や遷移が指定されているとは限らないため、完全指定された有限状態機械の状態同値性をそのまま適用することはできない。そこで、二状態が互いに両立可能かを調べるcompatibility relationを用い、compatible classesを構成して状態数を削減する方法が研究されてきた。この枠組みは、その後の有限状態機械理論においても標準的な状態簡約問題として扱われている（Paull and Unger, 1959; Kohavi and Jha, 2009）。

古典的なincompletely specified FSM minimizationでは、単に同一クラス内の状態が現在のinput-output条件についてcompatibleであるだけでは十分ではない。縮約されたmachineをその後も再帰的に運用するためには、選択されたクラスの後続状態も縮約されたクラス構造と整合しなければならない。このため、compatible classesだけでなく、後続状態に関するclosure条件を満たすcoverを求める必要が生じる。

本研究のABCWデータも、部分指定されたinput-output behaviorという点ではこれと類似した構造を持つ。

現在場を $${\Delta W}$$、行動条件を $${a}$$、一時刻先の完全場を出力とみなせば、観測データは概念的には

$${(\Delta W,a)\longmapsto\Delta W'}$$

という部分指定されたinput-output tableとして読むことができる。

このとき、二つの現在場 $${\Delta W_i,\Delta W_j}$$ が同じ行動条件 $${a}$$ のもとで観測され、異なる次場

$${\Delta W_i'\neq\Delta W_j'}$$

を生成するならば、両者を同じfield classへまとめることはできない。

そこで本研究では、2,562種類の現在場を頂点とし、

> **ある共通の行動条件のもとで異なる次場を生じる二場を結ぶ**

incompatibility graphを構成する。

このグラフ上で隣接する二頂点は同じfield classへ入れられないため、100%の一時刻先完全場予測を保存するfield-only partitionはproper coloringに対応する。

逆に、incompatibility graphのproper coloringが与えられれば、同じ色を持つ二場の間には、観測されたどの共通行動条件についても異なる次場を生じるconflictが存在しない。したがって各色を一つのfield classとみなすことで、

$${\bigl(a_t,B(\Delta W_t)\bigr)\longrightarrow\Delta W_{t+1}}$$

の一価性が保たれる。

したがって必要な最小クラス数は、

$${|\operatorname{Im}B_{\min}|=\chi(G)}$$

としてchromatic numberへ正確に帰着される。

ここで、古典的なincompletely specified FSM minimizationとの重要な違いがある。

本研究では、得られたfield classを次時刻の新しい内部状態として再帰的に運用することを要求しない。保存対象は縮約後のclass labelではなく、生の一時刻先完全場 $${\Delta W_{t+1}}$$ そのものである。

すなわち本稿で要求するのは、

$${\bigl(a_t,B(\Delta W_t)\bigr)\longrightarrow\Delta W_{t+1}}$$

というdepth-1のtarget predictionが一価であることだけである。

このため、古典的なmachine minimizationで必要となる後続クラスについてのrecursive closureを本問題では課す必要がない。必要条件は、同じfield classへ割り当てる二場の間に観測されたinput-output conflictが存在しないことに尽きる。

その結果、本研究で設定したdepth-1 prediction problemでは、最小化問題がclosed-cover constructionではなく、incompatibility graphのproper coloringへ直接帰着する。

また、この定式化ではcompatibility relationそのものを同値関係として仮定する必要がない。部分指定データでは「衝突しない」というcompatibilityは一般に推移的とは限らないが、本研究では同一クラスに入れることのできない頂点対をincompatibility edgeとして直接表現する。したがって、必要な制約はproper coloringのpairwise constraintとして扱われる。

この簡略化は、一般のincompletely specified FSM minimizationに対する新しい最小化理論を提案するものではない。むしろ、**保存対象を一時刻先の外部targetへ限定したABCWの予測問題では、古典的なrecursive closure requirementが不要となり、最小化が純粋なgraph-coloring problemとして表現できる**ことが、本稿の定式化上の特徴である。

## 2.6 Feature-based coarse-graining and predictive partitioning

本研究ではさらに、二種類の状態圧縮を区別する。

第一は、状態からあらかじめ選んだ特徴量を計算する方法である。

$${\Delta W\longrightarrow B_{\mathrm{feature}}(\Delta W)}$$

例えば、ノルム、局所構造、hub structure、out-strengthなどを用いて場を要約する方法がこれにあたる。

この方法の利点は、得られる観測量が人間に解釈しやすいことである。しかし、少数の特徴量で表現したこと自体は、真に状態を粗視化したことを意味しない。有限集合上では、低次元の特徴ベクトルであってもすべてのミクロ状態を一意に識別できる場合がある。

また、真に複数の状態を統合した場合には、その統合によって予測に必要な区別まで失われる可能性がある。

第二は、特徴量を先に選ばず、未来応答から必要な区別を逆算する方法である。

概念的には、

$${\Delta W\longrightarrow\left(a\longmapsto\Delta W'\right)}$$

という応答構造から分割を構成する。

本研究の692分割は後者に属する。

この方法では、得られたクラスが単純なネットワーク統計量として解釈できる保証はない。その代わり、指定された予測目的を保存するという条件から、どの区別が必要であるかを直接決定できる。

本稿ではこの性質を **predictive sufficiency** と呼ぶ。

ここでいうpredictive sufficiencyは、「少数の変数で状態を記述できる」という意味ではない。観測 $${P}$$ が指定された予測対象 $${Z}$$ に対してpredictively sufficientであるとは、対象とするデータ集合上で

$${P(X_t)\longrightarrow Z}$$

が一価となり、$${P(X_t)}$$ から $${Z}$$ を曖昧さなく決定できることをいう。

したがって、本研究で問題となるのは単なる表現次元の削減ではなく、

> **指定された予測対象を失わないために必要な区別を保持しながら、どこまで現在の区別を捨てられるか**

である。

## 2.7 Position of the present study

以上から、本研究には二つの異なる先行研究上の接続がある。

第一は、ABCWの競合的エージェント力学としての背景である。El FarolおよびMinority Gameとは、主体の利得が他主体の選択に依存し、全主体が同時に同じ意味で成功できない競合構造を共有する。ただし、本研究はMinority Gameの典型的な集団現象や戦略適応そのものを分析対象とはせず、その競合規則を場 $${W}$$ と主体行動の相互更新を生じさせる構成要素として用いる。

第二は、本稿の中心課題であるpredictive state reductionの理論的位置づけである。

lumpabilityとの関係では、粗視化後にもwell-definedな時間発展を求めるという問題意識を共有するが、本研究ではself-closureとtarget predictionを区別する。

bisimulationおよびMDP minimizationとの関係では、将来挙動を保存する状態集約という発想を共有するが、最適方策や縮約されたMDP全体を保存することを目的としない。

computational mechanicsとの関係では、未来予測に必要な区別だけを残すという発想を共有するが、本研究の692クラスは履歴に基づくcausal statesではなく、有限到達集合上の一時刻先・行動条件付きfield responseを保存する分割である。

incompletely specified finite-state machine minimizationとは、部分指定されたinput-output behaviorにおけるcompatibility / incompatibilityという点で、より直接的な数学的対応を持つ。本研究では、保存対象を一時刻先の完全場に限定することでrecursive closureを要求しないdepth-1 prediction problemとしてこの構造を用いる。

したがって、本研究の位置づけを最も限定的に述べれば、

> **競合的な有限エージェント力学から得られた部分指定input-output dataに対して、指定された一時刻先予測を完全に保存するfield-only partitionの厳密最小値を求める具体的なstate-minimization problem**

である。

本研究の新規性を、Minority Game、state minimization、predictive representationのいずれかの一般的な考え方そのものに求めることはしない。

本稿が示す具体的な結果は、5主体ABCWの今回観測された有限到達集合において、このdepth-1 prediction problemを明示的に構成し、そのincompatibility graphについて、

$${\chi(G)=692}$$

を上界構成と独立な下界によって厳密に確定できることである。

これにより、2,562種類のミクロに異なる場すべてを保持することなく、一時刻先の完全な場を100%予測できる一方、691クラス以下ではその予測を完全には保存できないことが示される。

この具体例を通じて、本稿では「状態として異なること」と「指定された未来を予測するために区別する必要があること」の間にある差を、有限かつ完全に検査可能な形で調べる。

---

# 3. ABCW Model and Dataset

本節では、本論文で解析する5主体ABCWモデルと、後続の予測分割問題に用いる有限到達データセットを定義する。ここでの目的はABCWの探索過程を再現することではなく、後の解析に必要な状態変数、更新則、場の表現、および解析対象の範囲を固定することである。

## 3.1 State Variables and Interaction Network

主体集合を

$${V=\lbrace1,\ldots,n\rbrace}$$

とし、本論文では

$${n=5}$$

を用いる。各主体 $${i}$$ は時刻 $${t}$$ に二値の行動

$${a_i(t)\in\lbrace-1,+1\rbrace}$$

と二値の戦略

$${s_i(t)\in\lbrace-1,+1\rbrace}$$

を持つ。$${s_i(t)=+1}$$ は参照信号に従う戦略、$${s_i(t)=-1}$$
は参照信号に反する戦略を表す。

主体間の影響関係は、固定トポロジー

$${E=(E_{ij}),\qquad E_{ij}\in\lbrace0,1\rbrace}$$

と、時間変化する非負の重み行列

$${W(t)=(w_{ij}(t))}$$

によって表す。$${E_{ij}=1}$$ は有向辺 $${i\to j}$$
が存在しうることを意味し、$${w_{ij}(t)}$$ はその時点で主体 $${i}$$
が主体 $${j}$$
に与える影響の強さを表す。重みが0になっても、$${E_{ij}=1}$$
である限りトポロジー上の辺そのものは削除しない。

戦略を状態変数として含めるため、完全状態を

$${X(t)=(a(t),s(t),W(t))}$$

と定義する。

Table 1に、本論文で主に用いる変数をまとめる。

## Table 1. ABCW variables and update-rule summary

| Symbol        | Meaning          | Domain / type                        | Role / update                                             |
|:--------------|:-----------------|:-------------------------------------|:----------------------------------------------------------|
| $a_i(t)$      | Action           | $\{-1,+1\}$                          | Current binary action                                     |
| $s_i(t)$      | Strategy         | $\{-1,+1\}$                          | Trend-following / contrarian; loser flips strategy        |
| $u_i(t)$      | Payoff           | $\{-1,+1\}$ for n=5                  | Minority +1, majority -1; all-same gives -1               |
| $W(t)$        | Influence field  | nonnegative weighted directed matrix | Outgoing edges updated by source payoff                   |
| $\sigma_i(t)$ | Reference signal | $[-1,1]$                             | Mean action among strongest effective incoming references |
| $\Delta W(t)$ | Field deviation  | matrix                               | $W(t)-W^*$                                                |

## 3.2 Payoff, Reference Signal, and Update Rules

### 3.2.1 Minority-game payoff

各時刻に全主体が $${-1}$$ または $${+1}$$
のいずれかを選ぶ。少数派に属する主体を勝者、多数派に属する主体を敗者とし、利得を

$${u_i(t)\in\lbrace-1,+1\rbrace}$$

で表す。少数派では $${u_i(t)=+1}$$、多数派では $${u_i(t)=-1}$$
とする。本論文では $${n=5}$$
が奇数であるため、二値行動の人数が同数になることは原理的にない。全主体が同じ行動を選んだ場合には、全員を敗者として
$${u_i(t)=-1}$$ とする。

この利得規則は標準的なMinority
Game全体を再現するためではなく、「全員が同時には勝てない」という競合性をABCWへ導入するために用いる。

### 3.2.2 Reference signal

主体 $${i}$$ が参照可能な主体集合を

$${\mathcal N_i=\lbrace j\in V\mid E_{ji}=1\rbrace}$$

とする。その中で主体 $${i}$$ へ入る最大重みを

$${m_i(t)=\max_{j\in\mathcal N_i}w_{ji}(t)}$$

とし、その最大値を持つ主体集合を

$${M_i(t)=\lbrace j\in\mathcal N_i\mid w_{ji}(t)=m_i(t)\rbrace}$$

とする。

$${m_i(t)>0}$$ のとき、参照信号を

$${\sigma_i(t)=\frac{1}{|M_i(t)|}\sum_{j\in M_i(t)}a_j(t)}$$

と定義する。最大重みを持つ主体が複数存在する場合には一主体を任意に選ばず、同率の主体を等しく参照する。参照行動が拮抗した場合には
$${\sigma_i(t)=0}$$
となる。また、参照可能な主体が存在しない場合、または最大影響力が0の場合も、有効な参照信号なしとして
$${\sigma_i(t)=0}$$ と扱う。

したがって、ゲームの勝敗 $${u_i(t)}$$
は全主体の行動から決まる一方、次の行動に用いる参照情報 $${\sigma_i(t)}$$
は局所的な影響関係から決まる。

### 3.2.3 Strategy adaptation

本論文で用いる適応版ABCWでは、主体は直前の一ゲームの勝敗だけを用いて戦略を更新する。勝者は戦略を維持し、敗者は戦略を反転する。したがって、

$${s_i(t+1)=
\begin{cases}
s_i(t),&u_i(t)=+1,\cr
-s_i(t),&u_i(t)=-1
\end{cases}}$$

であり、簡潔には

$${s_i(t+1)=u_i(t)s_i(t)}$$

と書ける。

### 3.2.4 Action update

現在の行動から利得を計算し、現在の場から参照信号を計算した後、まず戦略を更新する。敗者はこの**更新後の戦略**を用いて次の行動を決める。したがって、適応版では行動更新を

$${a_i(t+1)=
\begin{cases}
a_i(t),&u_i(t)=+1,\cr
a_i(t),&u_i(t)=-1,\ \sigma_i(t)=0,\cr
\operatorname{sgn}\!\left(s_i(t+1)\sigma_i(t)\right),&u_i(t)=-1,\ \sigma_i(t)\neq0
\end{cases}}$$

と書く。

すなわち、勝者は現在行動を維持する。敗者については、有効な参照信号がなければ現在行動を維持し、有効な参照信号があれば更新後の戦略に従って次行動を選ぶ。

### 3.2.5 Field update

最後に利得を場へ反映する。一般には学習率を $${\eta>0}$$ とし、本稿で解析する全実験では $${\eta=1}$$ を用いる。

$${w_{ij}(t+1)=
\begin{cases}
\max\!\left(0,w_{ij}(t)+\eta u_i(t)\right),&E_{ij}=1,\cr
0,&E_{ij}=0
\end{cases}}$$

とする。したがって主体 $${i}$$
が勝てば、その主体から出る既存辺の重みが増加し、負ければ減少する。

一ゲームの更新順序は、

$${\begin{array}{c}
(a(t),s(t),W(t))\cr
\downarrow\cr
u(t),\sigma(t)\cr
\downarrow\cr
s(t+1)\cr
\downarrow\cr
a(t+1)\cr
\downarrow\cr
W(t+1)
\end{array}}$$

で固定する。この順序は、敗者が更新前ではなく更新後の戦略を用いるため、モデル定義の一部である。

![Figure 2. ABCW update cycle. Update order for the adaptive five-agent ABCW model used to construct the dataset. Payoffs and reference signals are computed from the current state; strategies are updated, then actions, then the influence field.](figures/Fig2_ABCW_update_cycle.png)

*Figure 2. ABCW update cycle. Update order for the adaptive five-agent ABCW model used to construct the dataset. Payoffs and reference signals are computed from the current state; strategies are updated, then actions, then the influence field.*

## 3.3 Field Representation

5主体の完全対称な基準場を

$${W^\ast=
\begin{array}{ccccc}
0&1&1&1&1\cr
1&0&1&1&1\cr
1&1&0&1&1\cr
1&1&1&0&1\cr
1&1&1&1&0
\end{array}}$$

とする。$${W^\ast}$$
は均衡状態や自然な社会状態を意味するものではなく、場の変形を記述するための基準点である。

現在場の基準場からの差を

$${\Delta W(t)=W(t)-W^\ast}$$

と定義する。成分ごとには

$${\Delta w_{ij}(t)=w_{ij}(t)-w^\ast_{ij}}$$

である。したがって $${\Delta W(t)=0}$$
は現在場が基準場と一致することを表す。

ここで $${\Delta W\neq0}$$ は、必ずしも行列の非対称性
$${W\neq W^{\mathsf T}}$$ を意味しない。本論文でいうfield
deviationは、基準場からの差そのものを指す。後続の予測問題では、この
$${\Delta W}$$ をfield variableとして扱う。

## 3.4 Dataset Construction

解析には、5主体ABCWについて4種類の初期場を用いる。

-   baseline
-   Hub
-   Local
-   Hub+Local

baselineは $${W(0)=W^\ast}$$
とする。他の3初期場では、同じ更新則を保ったまま、基準値1の有向辺4本を4へ強化し、強い辺の配置だけを変える。主体番号を $${1,\ldots,5}$$ とし、有向辺 $${i\to j}$$ を $${(i,j)}$$ と書けば、強化辺は次の通りである。

- Hub：$${(1,2),(1,3),(1,4),(1,5)}$$
- Local：$${(1,2),(2,3),(3,4),(4,5)}$$
- Hub+Local：$${(1,3),(1,5),(2,3),(4,5)}$$

すなわちHubでは主体1から他4主体への出辺を強化し、Localでは連鎖状の4辺を強化し、Hub+Localでは主体1からの2辺と、それらと同じ到達先を持つ2本の局所競合辺を組み合わせる。したがってこれら3場では、非零の初期偏差成分は4個であり、

$${\lVert\Delta W(0)\rVert_F=\sqrt{4\times3^2}=6}$$

で共通する。これらはネットワーク構造の全分類を意図したものではなく、異なる場配置から到達する有限状態集合を構成するための初期条件群として用いる。

各初期場について、5主体の初期行動 $${a(0)}$$ と初期戦略 $${s(0)}$$
の全組合せを調べる。各成分は二値なので、一初期場あたり

$${2^5\times2^5=1024}$$

条件であり、4初期場の総初期条件数は

$${4\times1024=4096}$$

である。

各ケースを完全状態が再訪するまで時間発展させ、その途中に現れる遷移を収集した。この手続きによって得られた解析対象は56,536遷移であり、そこには2,562種類の異なる現在場
$${\Delta W}$$ と、11,202種類の異なる $${(a,\Delta W)}$$ が含まれる。

## Table 2. Dataset construction and summary

| Quantity                          |   Value |
|:----------------------------------|--------:|
| Agents                            |       5 |
| Learning rate $\eta$              |       1 |
| Initial field configurations      |       4 |
| Action configurations per field   |      32 |
| Strategy configurations per field |      32 |
| Initial conditions                |    4096 |
| Observed transitions              |   56536 |
| Distinct current fields           |    2562 |
| Distinct $(a,\Delta W)$ states    |   11202 |

重要なのは、56,536遷移がABCWの理論上の全状態空間を意味しないことである。本論文の後続結果は、上記4初期場と4,096初期条件から到達し、保存されたこの有限遷移集合に対する結果として解釈する。未到達状態、他の主体数、他の初期場に対する一般化は主張しない。また、今回の4,096条件で全軌道が再訪したという事実を、重みが一般に有界であることの証明とは解釈しない。

------------------------------------------------------------------------

# 4. Observation and Predictive Objective

本節では、前節で定義した有限ABCW力学に対して、「現在のどの違いを残せば、指定した未来を完全に予測できるか」という問題を定式化する。ここで重要なのは、観測自身の時間発展が閉じることと、特定の予測対象を決定できることを区別することである。

## 4.1 Observation as Information Loss

完全状態空間を $${\Omega}$$ とし、観測を写像

$${P:\Omega\longrightarrow Y}$$

として表す。異なる完全状態 $${X,X'\in\Omega}$$ が

$${P(X)=P(X')}$$

を満たすとき、観測 $${P}$$ は両者の違いを捨て、同じ観測状態として扱う。

したがって本論文では、観測を単に「どの変数を見るか」という選択ではなく、**完全状態のどの区別を保持し、どの区別を同一視するかを定める写像**として扱う。

ABCWの完全状態は

$${X=(a,s,W)}$$

である。基準場 $${W^\ast}$$ は固定されているので、$${W}$$ と
$${\Delta W}$$ は一対一に対応する。したがって、例えば

$${P_W(X)=\Delta W}$$

は行動 $${a}$$ と戦略 $${s}$$ の違いを捨てる観測であり、

$${P_{aW}(X)=(a,\Delta W)}$$

は戦略 $${s}$$ の違いだけを捨てる観測である。

## 4.2 Self-Closure and Target Prediction

ABCWの決定論的更新を

$${X_{t+1}=\Phi(X_t)}$$

と書く。観測 $${P}$$ について、

$${P(X)=P(X')}$$

なら常に

$${P(\Phi(X))=P(\Phi(X'))}$$

となるとき、観測状態だけで次の観測状態が一意に定まる。本論文ではこの性質をself-closureと呼ぶ。この条件は、粗視化後の状態遷移をwell-definedにする決定論的なquotient-consistency条件であり、lumpabilityやbisimulationにおける状態集約条件と近縁である。一方、未来系列の条件付き分布から状態を定義するcausal
statesそのものとは同一ではない（Shalizi and Crutchfield, 2001; Givan et
al., 2003）。

しかし、self-closureは特定の予測目的に対する十分性とは異なる。未来について知りたい量を

$${Z=g(X_{t+1})}$$

とすれば、必要なのは

$${P(X_t)\longrightarrow Z}$$

が一価であることであり、必ずしも

$${P(X_t)\longrightarrow P(X_{t+1})}$$

が一価である必要はない。

この区別は今回の有限データ上で実際に現れる。field-only observation

$${P_W(X)=\Delta W}$$

では、観測された2,562種類の現在場のうち、一時刻先の場が一意だったのは1,390種類であり、

$${\frac{1390}{2562}\simeq0.54254}$$

すなわち約54.3%であった。したがって現在場だけでは、一時刻先の完全な場を一般には決定できない。

一方、

$${P_{aW}(X)=(a,\Delta W)}$$

と現在行動を保持すると、

$${(a_t,\Delta W_t)\longrightarrow\Delta W_{t+1}}$$

は、今回観測された11,202種類の $${(a,\Delta W)}$$
すべてで一意であった。これに対し、

$${(a_t,\Delta W_t)\longrightarrow(a_{t+1},\Delta W_{t+1})}$$

という観測自身の次状態については、11,202観測状態中8,390状態だけが一価であり、

$${\frac{8390}{11202}\simeq0.748973}$$

すなわち約74.9%であった。

したがって、**自分自身の次状態についてself-closedでない観測でも、指定した未来だけなら完全に予測できる**。本論文では以後、この二つを分離し、予測対象を明示的に固定する。

## 4.3 One-Step Exact-Field Prediction

本論文の予測対象を

$${Z=\Delta W_{t+1}}$$

とする。すなわち、現在の観測から一時刻先の**完全なfield
deviation**を誤差なく予測することを要求する。

前節の有限データでは、$${(a_t,\Delta W_t)}$$
を保持すればこの予測は100%一価である。しかし、この観測は2,562種類のfield
deviationをそのまま保持している。そこで、現在行動 $${a_t}$$
は保持したまま、field側だけをさらに粗くする。

field-only mapを

$${B:\Delta W\longrightarrow\mathcal C}$$

とし、対応する観測を

$${P_B(X_t)=\left(a_t,B(\Delta W_t)\right)}$$

と定義する。

$${B}$$
が本論文の予測要件を満たすとは、解析対象となる全遷移について、任意の二つの現在状態
$${X_t,X'_t}$$ が

$${a_t=a'_t}$$

かつ

$${B(\Delta W_t)=B(\Delta W'_t)}$$

を満たすなら、

$${\Delta W_{t+1}=\Delta W'_{t+1}}$$

が成り立つこととする。言い換えれば、

$${\left(a_t,B(\Delta W_t)\right)\longrightarrow\Delta W_{t+1}}$$

が保存された有限遷移集合上で一価であることを要求する。

ここでは、action $${a}$$
自体は圧縮対象に含めない。また、予測対象も粗視化せず、一時刻先の完全な
$${\Delta W}$$
をそのまま要求する。したがって本論文で扱う問題は、**action-conditioned,
one-step, exact-output, field-only predictive partition**
の最小化問題である。

本論文では、この一価性を指定された予測対象に対する**predictive
sufficiency（予測十分性）**と呼ぶ。すなわち本節では、$${(a_t,B(\Delta W_t))}$$
が $${\Delta W_{t+1}}$$ に対してpredictively sufficientであることを
$${B}$$ の要件とする。

## 4.4 Minimum Field Partition

$${B}$$ によって同じ値へ写されるfield
deviationを同一クラスとみなし、そのクラス集合を $${\operatorname{Im}B}$$
とする。

完全なfield observationでは

$${|\operatorname{Im}B|=2562}$$

である。予測性能を100%に保ったまま

$${|\operatorname{Im}B|<2562}$$

を実現できれば、少なくとも今回の有限到達集合上では、異なる複数のfield
deviationを予測上同一視できる。

そこで本論文の最適化問題を、

$${\min_B|\operatorname{Im}B|}$$

subject to

$${\left(a_t,B(\Delta W_t)\right)\longrightarrow\Delta W_{t+1}\quad\text{is single-valued on all observed transitions}}$$

と定義する。

この最適化は、関連情報を保持しながら表現を圧縮するInformation
Bottleneckの問題意識とは近いが、標準的Information
Bottleneckの目的関数そのものではない。標準形が相互情報量による圧縮と関連情報保持のtrade-offを最適化するのに対し、本論文では予測誤差0をhard
constraintとして固定し、有限集合上の**クラス数**
$${|\operatorname{Im}B|}$$ を最小化する（Tishby et al.,
2000）。また、self-closureの最粗分割を求める問題とも異なり、ここでは保持したactionを条件として外部target
$${\Delta W_{t+1}}$$
を保存する。したがって、本節の最小化はself-closureの最粗分割を求める問題とは区別して扱う。

必要に応じて、field class数に基づく圧縮率を

$${C_{\Delta W}=1-\frac{|\operatorname{Im}B|}{2562}}$$

とする。ただしこれはクラス数ベースの圧縮率であり、Shannon情報量や必要ビット数の削減率を意味しない。

この定式化によって、問題は「自然に見える特徴量を先に選ぶ」ことから切り離される。次節ではまず自然なnetwork
featuresを用いたbaselineを調べ、その後、予測条件そのものから必要なfield
distinctionを逆算して最小分割を求める。

---

# 5. Natural-Feature Baselines

本節では、最小予測分割を力学から直接構成する前に、ノルム、局所構造、hub structure、out-strengthなど、人間があらかじめ選んだネットワーク特徴量によって現在場 $${\Delta W}$$ をどこまで粗く記述できるかを検討する。目的は、特徴量の解釈可能性と、真のfield compressionおよび一時刻先完全場のpredictive sufficiencyがどこまで両立するかを確認することである。

## 5.1 Natural-feature compression and its limit

たとえばout-strengthは非常に高い予測性能を示した。ここで状態単位の決定率は、$${(a,\mathrm{out\mbox{-}strength})}$$ によって定義される観測状態を単位として評価した。11,142個の観測状態のうち11,084状態では次場が一意に定まり、

$${\frac{11084}{11142}=0.994794\ldots}$$

すなわち99.4794%の状態単位決定率を得た。残る58状態では、同一の観測状態から複数の次場が観測された。

この値の分母は遷移総数56,536ではなく、異なる観測状態の数11,142である。したがって、後述する遷移集合全体に対する評価とは区別される。

しかし、残された58個の衝突状態を解消しながら真に $${\Delta W}$$ を圧縮する単純な特徴量の組を探索しても、検討した候補集合の範囲では、圧縮と100%の予測決定性を同時に満たす特徴量は得られなかった。

一方、Sec. 6で厳密に構成する未来応答ベースの最小予測分割は、2,562個の場を692クラスへ圧縮しながら、観測された56,536遷移について一時刻先の場を完全に区別する。

ここには二種類の圧縮の違いがある。

一つは、

$${\Delta W\longrightarrow B(\Delta W)}$$

という形で、人間があらかじめ選んだ特徴量によって場を要約する方法である。

もう一つは、

$${\Delta W\longrightarrow
\left(a\longmapsto\Delta W'\right)}$$

という未来応答の同値性から、必要な区別を逆算する方法である。

前者は解釈しやすいが、予測情報を失う可能性がある。

後者は予測上必要な区別を直接保存するが、そのクラスに単純なネットワーク統計量としての意味が存在するとは限らない。

Sec. 6で示す692分割は後者に属する。

---




## 5.2 Exhaustive combinations of the candidate feature families

本研究で検討した9特徴族の非空部分集合は、

$${2^9-1=511}$$

通りである。これら511候補を全探索した範囲では、真に異なる $${\Delta W}$$ を統合するfield compressionと、一時刻先完全場の100%予測を同時に達成する候補は得られなかった。out-strength vectorは高い決定率を示したが58個の衝突観測状態を残し、100%予測に到達する特徴表現 $${B^*}$$ は2,562場をすべて一意に識別するため真のfield compressionではなかった。

## Table 3. Natural-feature baselines and exact minimum partition

| Observation                                                                                     |   Field classes |   Observed $(a,B)$ states |   $D_{state}$ |   $A_{freq}$ | True field compression   |
|:------------------------------------------------------------------------------------------------|----------------:|--------------------------:|--------------:|-------------:|:-------------------------|
| Full field $\Delta W$                                                                           |            2562 |                     11202 |      1        |     1        | No                       |
| out-strength vector                                                                             |            2516 |                     11142 |      0.994794 |     0.994658 | Yes                      |
| Best true-compression candidate by $D_{state}$ (in-strength distribution + out-strength vector) |            2561 |                     11200 |      0.999821 |     0.999717 | Yes                      |
| $B^*=(\|\Delta W\|_F^2,\mathrm{out\mbox{-}strength\ vector})$                                   |            2562 |                     11202 |      1        |     1        | No                       |
| Exact minimum partition $B_{692}$                                                               |             692 |                      8084 |      1        |     1        | Yes                      |


![Figure 3. Prediction performance versus actual field compression. All 511 nonempty combinations from the nine natural feature families are plotted using the number of distinct field values and the state-level determinism score. The out-strength vector, the 100%-predictive but noncompressive B* representation, the best genuinely compressive candidate by D_state, and the exact 692-class partition are highlighted.](figures/Fig3_prediction_vs_field_compression.png)

*Figure 3. Prediction performance versus actual field compression. All 511 nonempty combinations from the nine natural feature families are plotted using the number of distinct field values and the state-level determinism score. The out-strength vector, the 100%-predictive but noncompressive B* representation, the best genuinely compressive candidate by D_state, and the exact 692-class partition are highlighted.*


以上から、自然な特徴量の探索が100%予測と真のfield compressionを同時に達成できなかったことだけから、2,562種類の現在場をほぼすべて保持する必要があるとは結論できない。次節では特徴量を先に選ぶという制約を外し、未来の衝突関係から必要な区別を直接求める。

---

# 6. Exact Minimum Predictive Partition

## 6.1 Incompatibility graph

前節では、out-strengthをはじめとする自然なネットワーク特徴量を用いて、現在場 $${\Delta W}$$ をどこまで粗く記述できるかを調べた。

しかし、そこで用いた候補はすべて、人間があらかじめ選んだ特徴量から構成されたものである。したがって、その候補族の中に100%予測と真の場圧縮を同時に満たす観測が存在しなかったとしても、

> **一歩先の完全場を100%予測するために、2,562種類の現在場をほぼすべて区別する必要がある**

とは結論できない。

そこで本節では、特徴量を先に選ぶという制約を外し、

> **未来を取り違えないために、現在場のどの区別を残す必要があるか**

を力学から直接求める。

解析対象は前節までと同じ有限到達集合であり、

- 56,536 transitions
- 2,562 distinct current fields
- 11,202 distinct $${(a,\Delta W)}$$ states

を含む。

場だけに作用する写像

$${B:\Delta W\longrightarrow\mathcal C}$$

を考え、観測を

$${P_B(X_t)=(a_t,B(\Delta W_t))}$$

とする。

要求する条件は、観測された全56,536遷移について、

$${(a_t,B(\Delta W_t))\longrightarrow\Delta W_{t+1}}$$

が一価になることである。

すなわち、同じ行動 $${a}$$ と同じfield classから異なる次場が生じてはならない。

ここで二つの現在場 $${\Delta W_i,\Delta W_j}$$ を考える。ある共通の行動 $${a}$$ のもとで両者が観測され、それぞれが異なる一時刻先の場 $${\Delta W'_{i}\neq\Delta W'_{j}}$$ を生成するならば、両者を同じfield classへまとめることはできない。

もし

$${B(\Delta W_i)=B(\Delta W_j)}$$

とすると、同一の観測

$${(a,B(\Delta W_i))=(a,B(\Delta W_j))}$$

から二つの異なる次場が生じ、一歩先完全場予測の一価性が失われるからである。

そこで、2,562種類の現在場を頂点とし、

> **ある共通行動のもとで異なる次場を生じる二場の間に辺を張る**

incompatibility graph $${G}$$ を構成する。

このとき、100%予測を保存するfield-only分割は、$${G}$$ の隣接頂点に異なるラベルを割り当てるproper coloringに対応する。

したがって、求める最小field class数は、

$${|\operatorname{Im}B_{\min}|=\chi(G)}$$

として、incompatibility graphの彩色数へ帰着される。

この最小化問題は、抽象的なstate-minimizationそのものを新たに提案するものではない。部分指定されたinput-output behaviorに対するcompatibility / incompatibilityに基づく状態最小化、とくにdepth-1 partial Mealy machineとして既存のincompletely specified finite-state machine minimizationへ接続できる。本研究で求めるのは、その既存問題形式をABCWの有限到達力学へ適用したときに得られる具体的な厳密解である。

---

## 6.2 Constructive upper bound

まず、incompatibility graph $${G}$$ に対してDSATURによる彩色を行った（Brélaz, 1979）。

その結果、692色による有効なproper coloringが得られた。

したがって、

$${\chi(G)\le692}$$

である。

ただし、彩色アルゴリズムが692色を返したことだけでは、それが実際に元の予測問題を満たしていることの確認にはならない。

そこで、得られた692色をfield-only観測

$${B_{692}(\Delta W)}$$

として元の56,536遷移へ戻し、

$${(a,B_{692}(\Delta W))\longrightarrow\Delta W_{t+1}}$$

の一価性を直接検査した。

結果は、

- field classes：692
- distinct $${(a,B_{692})}$$ states：8,084
- nondeterministic observed states：0
- one-step complete-field prediction：100%

であった。

したがって、

$${2562\longrightarrow692}$$

というfield compressionを行いながら、一歩先の完全場予測を100%保存するfield-only分割が実際に存在する。

field class数に基づく圧縮率は、

$${C_{\Delta W}=1-\frac{692}{2562}\simeq0.7299}$$

であり、約72.99%である。

また、完全観測 $${(a,\Delta W)}$$ の11,202状態は、

$${(a,B_{692}(\Delta W))}$$

では8,084状態まで減少する。

以上から、692は求める最小値の上界である。

$${\boxed{\chi(G)\le692}}$$

しかし、この段階では691色以下のproper coloringが存在する可能性は排除されていない。

692が厳密な最小値であることを示すには、これとは独立に692以上の下界を構成する必要がある。

---

## 6.3 Anchor lower bound

下界を得るため、一つの行動条件を固定する。

アンカー行動として、

$${a=(-,-,-,-,-)}$$

を選ぶ。

このアンカー行動のもとで観測された現在場は1,239種類であり、それらは625種類の異なる次場へ進む。

したがって、以下の下界証明は2,562種類の現在場全体をアンカー群が覆うことを仮定しない。アンカー行動のもとで実際に観測された1,239頂点からなる部分グラフだけを用いて下界を構成する。

同じアンカー行動のもとで異なる次場へ進む二つの現在場は、同じfield classへ入れることができない。

よって、次場ごとに1,239場を625個のアンカー未来群

$${V_1,\ldots,V_{625}}$$

へ分けると、異なる群に属する任意の二頂点はincompatibility graph $${G}$$ 上で隣接する。

この事実を、次の補題として明示する。

### Lemma 1 — Additivity across anchor groups

異なるアンカー未来群 $${V_i,V_j}$$、$${i\neq j}$$ に対して、

$${u\in V_i,\quad v\in V_j}$$

ならば、アンカー行動のもとで $${u}$$ と $${v}$$ は異なる次場を生成する。

したがって、

$${\lbrace u,v\rbrace\in E(G)}$$

であり、異なるアンカー未来群は互いにcomplete joinをなす。

このため、proper coloringにおいて異なるアンカー群が同じ色を共有することはできない。

各群の誘導部分グラフを

$${G_i=G[V_i]}$$

とすると、アンカー観測部分グラフについて、

$${\chi\left(G\left[\bigcup_{i=1}^{625}V_i\right]\right)=\sum_{i=1}^{625}\chi(G_i)}$$

が成立する。

特に各群は少なくとも1色を必要とするため、

$${\chi(G)\ge625}$$

である。

したがって、この時点で、

$${\boxed{625\le\chi(G)\le692}}$$

まで範囲が狭まる。

しかし625は、一つのアンカー行動だけから見える区別である。

同じアンカー未来へ進む二場であっても、別の行動条件のもとでは異なる未来へ進む場合がある。その場合、アンカー行動だけなら同一視できる二場を、全行動条件を同時に満たすためにはさらに分離しなければならない。

そこで、625個のアンカー未来群それぞれについて、群内部に残るincompatibilityを調べた。

その結果、

- internal conflictsなし：575 groups
- internal conflictsあり：50 groups

であった。

575群では $${\chi(G_i)=1}$$ であり、追加分割は必要ない。

残る50群について、その内部彩色数を厳密に求める。

---



![Figure 4. Global sign-flip symmetry. Under the global action flip a -> -a, minority-game payoffs are unchanged and the one-step field update is invariant, so a and -a witness exactly the same field-conflict edges. Hence 30 non-anchor actions collapse to 15 global-flip orbits.](figures/Fig4_global_sign_flip_symmetry.png)

*Figure 4. Global sign-flip symmetry. Under the global action flip a -> -a, minority-game payoffs are unchanged and the one-step field update is invariant, so a and -a witness exactly the same field-conflict edges. Hence 30 non-anchor actions collapse to 15 global-flip orbits.*

この対称性により、行動 $${a}$$ と $${-a}$$ は同一のfield-conflict edge集合を証言する。したがって30個の非アンカー行動は、内部衝突を記述するうえでは15個のglobal-flip orbitへまとめられる。この対称性自体が692の下界を与えるわけではないが、どの行動条件が同じ衝突情報を重複して担っているかを明示し、後続の50群の内部解析を解釈するための冗長性除去と整合性チェックを与える。

## 6.4 Exact refinement of the 50 difficult anchor groups

内部衝突を含む50個のアンカー群について、それぞれの誘導incompatibility graph $${G_i}$$ のchromatic numberを厳密に計算した。

厳密彩色では、各群についてまずDSATURによるgreedy coloringから上界を求め（Brélaz, 1979）、Bron–Kerbosch型のmaximum-clique探索から下界を求めた（Bron and Kerbosch, 1973）。

下界と上界が一致した場合、その値を直ちに

$${\chi(G_i)}$$

とした。

一致しない場合には、その下界から上界までの各 $${k}$$ についてDSATUR順序を用いたbacktrackingによる $${k}$$-colorability判定を行い、彩色可能となる最小の $${k}$$ を求めた。

したがって、ここで用いる $${\chi(G_i)}$$ はgreedy coloringが返した色数ではなく、各誘導部分グラフについて下界と彩色可能性を照合して確定した厳密値である。

50群を含む625群全体で得られたchromatic-number distributionは、

- $${\chi=1}$$：575 groups
- $${\chi=2}$$：39 groups
- $${\chi=3}$$：8 groups
- $${\chi=4}$$：2 groups
- $${\chi=7}$$：1 group

であった。

特に最大の彩色数を要求した $${\chi=7}$$ の群は、44頂点・224内部衝突辺を持つ。この群ではmaximum cliqueによる下界とDSATURによる上界がともに7となり、

$${\chi(G_i)=7}$$

が直接確定した。

各群の頂点数、内部衝突辺数、厳密彩色数、下界、上界は再現用データに保存した。

Lemma 1より、異なるアンカー未来群の色集合は共有できない。

したがって、アンカー観測部分グラフに必要な総色数は各群のchromatic numberの和である。

625群を各1色とした基準から見れば、追加で必要になる色数は、

$${39(2-1)+8(3-1)+2(4-1)+1(7-1)}$$

$${=39+16+6+6}$$

$${=67}$$

である。

したがって、

$${625+67=692}$$

となる。

同じ結果は直接、

$${575\cdot1+39\cdot2+8\cdot3+2\cdot4+1\cdot7=692}$$

とクロスチェックできる。

よって、アンカー行動のもとで観測された1,239場からなる部分グラフだけですでに692色が必要である。

したがって全incompatibility graphについても、

$${\boxed{\chi(G)\ge692}}$$

が成立する。

ここで重要なのは、692という値がDSATURによって偶然得られた色数ではないことである。

625は一つのアンカー行動だけから強制される区別であり、残る67は、アンカー条件では同一視可能だった場の一部が、他の行動条件によってさらに分離されるために必要となる。

しかも、その追加区別は625群全体へ均等に分布しているのではなく、50群だけに局在している。

したがって、

$${692=625+67}$$

という分解は単なる算術的分解ではなく、incompatibility graphのcomplete-join構造と、各アンカー群内部に残るaction-conditioned conflictを反映している。 この上界と下界の一致、および $${625+67=692}$$ の分解をFigure 5に要約する。

---



## Table 4. Exact lower-bound decomposition

| Required colors per anchor group   |   Number of anchor groups |   Contribution to total classes |   Additional colors beyond one per group |
|:-----------------------------------|--------------------------:|--------------------------------:|-----------------------------------------:|
| 1                                  |                       575 |                             575 |                                        0 |
| 2                                  |                        39 |                              78 |                                       39 |
| 3                                  |                         8 |                              24 |                                       16 |
| 4                                  |                         2 |                               8 |                                        6 |
| 7                                  |                         1 |                               7 |                                        6 |
| Total                              |                       625 |                             692 |                                       67 |


![Figure 5. Exact minimum predictive partition. The constructive 692-coloring provides the upper bound. The anchor action yields 625 groups; exact coloring of the 50 internally conflicting groups requires 67 additional colors, producing a matching lower bound of 692.](figures/Fig5_exact_minimum_proof.png)

*Figure 5. Exact minimum predictive partition. The constructive 692-coloring provides the upper bound. The anchor action yields 625 groups; exact coloring of the 50 internally conflicting groups requires 67 additional colors, producing a matching lower bound of 692.*

## 6.5 Main result

Sec. 6.2では、全2,562場からなるincompatibility graphに対して692色の有効なproper coloringを実際に構成し、

$${\chi(G)\le692}$$

を得た。

さらに、その692-coloringを元の56,536遷移へ戻して検証し、

$${(a,B_{692}(\Delta W))\longrightarrow\Delta W_{t+1}}$$

が全観測遷移上で一価であることを確認した。

一方、Sec. 6.3–6.4では、アンカー行動のもとで観測された1,239場を625未来群へ分解した。

異なる未来群がcomplete joinをなすことと、各群内部のchromatic numberを厳密に求めたことから、

$${\chi(G)\ge692}$$

を得た。

したがって、上下界は一致する。

$${\boxed{\chi(G)=692}}$$

よって、今回観測された有限到達集合について、次の結果が得られる。

> **Main Result.**  
> 5主体ABCWの今回観測された56,536遷移、2,562種類の現在場に対して、field-only観測
>
> $${B:\Delta W\longrightarrow\mathcal C}$$
>
> を用い、
>
> $${(a_t,B(\Delta W_t))\longrightarrow\Delta W_{t+1}}$$
>
> を全観測遷移上で100%一価に保つとき、必要なfield class数の厳密最小値は
>
> $${\boxed{|\operatorname{Im}B_{\min}|=692}}$$
>
> である。

これは、2,562種類の現在場をすべて保持する必要がないことを意味する。

一歩先の完全場 $${\Delta W_{t+1}}$$ を正確に予測するという目的に限れば、

$${2562\longrightarrow692}$$

まで現在場をまとめることができる。

field class数に基づく圧縮率は、

$${1-\frac{692}{2562}\simeq72.99\%}$$

である。

一方、691クラス以下へまとめれば、Sec. 6.3–6.4で用いたアンカー部分グラフだけでもproper coloringが不可能になる。したがって、少なくとも一つの共通行動条件のもとで異なる次場を生じる二場を同一視することになり、100%予測は失われる。

したがって692は、単なる高性能な圧縮候補ではなく、

> **今回の有限到達集合において、一歩先のaction-conditionedな完全場予測を保存する最小field-only分割のクラス数**

である。

この結果は、前節のnatural-feature baselinesとの対比も明確にする。

自然なネットワーク特徴量から出発した探索では、真の場圧縮と100%予測を同時に達成する候補は、調べた511候補の範囲では見つからなかった。しかし、それは100%予測そのものが細かな場識別を要求していたためではない。

特徴量という制約を外し、未来のincompatibilityから必要な区別を逆算すれば、2,562種類の場は692クラスまで縮約できる。

したがって、本解析が示すのは、

$${\boxed{\text{人間に自然な特徴量}\neq\text{予測に必要な最小区別}}}$$

ということである。

ただし、692はABCW一般に対する普遍的な状態数ではない。

この値は、

- 5主体
- 今回生成された有限到達集合
- 観測された56,536遷移
- field-only compression
- action $${a}$$ を保持
- one-step prediction
- exact $${\Delta W_{t+1}}$$ を予測対象とする

という条件のもとで得られた厳密解である。

別の初期条件、別の到達集合、別の主体数、複数歩先予測、あるいはより粗い予測対象 $${Q}$$ を採用すれば、必要な最小分割は変わりうる。

また、本結果が確定するのはchromatic number、すなわち**最小クラス数692**である。DSATURによって得られた具体的な692-coloringと、下界証明で用いたアンカー群分解から得られるminimum coloringが同一のpartitionであることは、本節の証明には必要なく、ここではその一意性を主張しない。

本節によって、最小クラス数そのものの探索は完了する。

しかし、

$${2562\longrightarrow692}$$

という数が確定したことと、その692クラスが何を表しているかを理解したことは同じではない。

次節では、

> **692クラスの内部で、どの場が同一視され、どの区別が行動条件によって要求されているのか**

を調べる。

とくに、$${625\longrightarrow692}$$ を生んだ67の追加区別の局在、field classのサイズ分布、区別を露出させる行動条件、およびそれらに存在する対称性を解析する。

---


# 7. Structure and Interpretation of the Minimum Partition

前節までの解析では、観測された $${2,562}$$ 個の場 $${\Delta W}$$ に対して、行動 $${a}$$ を条件として次時刻の場 $${\Delta W'}$$ を一意に予測するために必要な最小クラス数が $${692}$$ であることを示した。

この結果は、単に「2,562状態を692状態へ圧縮できた」という圧縮率の問題ではない。本節では、この $${692}$$ クラスがどのような構造を持ち、なぜ $${625}$$ クラスでは足りず、さらに $${67}$$ 個の区別が必要になったのかを調べる。

目的は、692個のクラスそれぞれに人間が理解しやすい意味を割り当てることではない。むしろ、**未来を保存するために必要な区別が、元のミクロな場の区別とどのような関係にあるのか**を明らかにすることである。

---

## 7.1 692は単なる状態数ではない

本研究で求めた分割は、観測された場 $${\Delta W}$$ の集合に対する任意のクラスタリングではない。

二つの場 $${\Delta W_i,\Delta W_j}$$ を同一クラスにまとめられるのは、観測された行動条件のもとで、それらを同一視しても次時刻の場を一意に決定できる場合に限られる。

したがって、本研究で扱う分割は、

$${B:\Delta W\longrightarrow \lbrace1,\ldots,K\rbrace}$$

という写像のうち、

$${\bigl(a_t,B(\Delta W_t)\bigr)\longrightarrow \Delta W_{t+1}}$$

が観測データ上で一価となるものを対象としている。

その最小クラス数が

$${K_{\min}=692}$$

であった。

ここで重要なのは、692という数値それ自体に普遍的意味を与えないことである。この値は、本研究で固定した5主体ABCWモデル、4種類の初期場、そこから得られた有限の到達集合、および一時刻先の場 $${\Delta W_{t+1}}$$ を予測対象とするという条件のもとで得られた値である。

したがって以下では、692をABCW一般の普遍的なマクロ状態数とは呼ばず、**本データ集合において一時刻先の行動条件付き場応答を保存する最小予測分割**として扱う。

---

## 7.2 圧縮は実際に起きている

元の観測集合には $${2,562}$$ 種類の異なる $${\Delta W}$$ が存在する。

恒等観測

$${P_{\mathrm{id}}(\Delta W)=\Delta W}$$

を用いれば、当然ながらこれらをすべて区別するため、クラス数は2,562である。

これに対して最小予測分割では、

$${2562\longrightarrow692}$$

まで区別を減らすことができる。

すなわち、場のクラス数という意味では約73%の区別を捨てても、観測された範囲における一時刻先の場予測は失われない。

この圧縮は、少数の巨大クラスだけによって生じているわけではない。

692クラスのうち、

- 352クラスは単一の $${\Delta W}$$ のみを含む
- 340クラスは複数の $${\Delta W}$$ を含む
- 最大クラスは65個の異なる $${\Delta W}$$ を含む

という構造を持つ。

したがって、完全に区別しなければならない場が多数残る一方で、ミクロには異なる複数の場を予測上同一視できる場合も広範に存在する。

これは、

$${\text{ミクロ状態として異なる}}$$

ことと、

$${\text{未来予測のために区別する必要がある}}$$

ことが一致しないことを、具体的な有限モデル上で示している。

---

## 7.3 625クラスはどこから現れるか

692という最小値の内部構造を理解するうえで重要なのが、その直前に得られる $${625}$$ という下限である。

この下限を構成するため、単一のアンカー行動

$${a=(-,-,-,-,-)}$$

を固定した。この行動条件のもとで観測された現在場は1,239種類であり、それらから生じる異なる次場は625種類であった。そこで、同じ次場を与える現在場を同一群としてまとめることで、625群からなる初期分割を構成した。

この625分割を、アンカー行動以外を含む他の観測された行動条件について検査すると、そのままでは完全な予測分割にはならない。

625群のうち575群は、それ以上分割する必要がない。

問題が生じるのは残る50群だけである。

すなわち、

$${625=575+50}$$

であり、692への増加は全体に均等に生じるのではなく、この50群に局在している。

---

## 7.4 追加の67区別

50個の困難な群を、すべての行動条件について未来を一意に保つようさらに分割すると、追加で67個の区別が必要になる。

したがって、

$${625+67=692}$$

となる。

この追加分解後、50群の内部構造は、

$${39\times2+8\times3+2\times4+1\times7=117}$$

個のサブクラスとなる。

元の50群が117群へ分かれるため、増加数は

$${117-50=67}$$

である。

ここで注目すべきなのは、692という複雑さのすべてが一様に必要なのではないという点である。

大部分の区別は625クラスの段階ですでに確定しており、残る予測上の曖昧さは比較的小さな部分集合に集中している。

したがって692は、

$${\text{大きな基本分割}+\text{局所的な追加分解}}$$

という内部構造を持つ。

これは、最小予測分割を単なる巨大なルックアップテーブルとして見る場合には見えにくい性質である。 Figure 6は、352個のsingleton classと340個のmulti-field classという最終分割の構成、および追加67区別が625アンカー群中50群に局在することをまとめて示す。

---



![Figure 6. Internal structure of the 692-class partition. Top: composition of the 692 predictive classes (352 singleton and 340 multi-field classes), with verified mean, median, and maximum class size. Bottom: localization of all additional refinements to 50 of the 625 anchor groups.](figures/Fig6_internal_structure_692.png)

*Figure 6. Internal structure of the 692-class partition. Top: composition of the 692 predictive classes (352 singleton and 340 multi-field classes), with verified mean, median, and maximum class size. Bottom: localization of all additional refinements to 50 of the 625 anchor groups.*

## 7.5 ミクロな近さと予測上の同一性

次に、同一クラスに属する場同士が、通常の意味で互いに「似ている」のかを調べた。

もし最小予測分割が単純な幾何学的クラスタリングに近いものであれば、同一クラスには互いに近い $${\Delta W}$$ が集まり、遠く離れた $${\Delta W}$$ は異なるクラスに属すると期待できる。

しかし、内部構造の検査では、この直観は一般には成立しなかった。

ミクロな表現上では比較的大きく異なる二つの場が同一予測クラスに属する場合がある一方で、互いに近い場であっても異なるクラスへ分離される場合がある。

したがって、692分割が保存しているのは $${\Delta W}$$ 空間そのものの幾何学ではない。

保存されているのは、

$${\Delta W_t\longmapsto
\left(a\longmapsto\Delta W_{t+1}\right)}$$

という**行動条件付き未来応答**である。

この意味で、二つの場の「近さ」は、その成分差の小ささではなく、未来に対して同じ応答を返すかどうかによって決まる。

---

## 7.6 predictive sufficiency と表現コスト

以上の結果は、本研究で導入した **predictive sufficiency** と圧縮の関係を具体化する。

恒等観測 $${P_{\mathrm{id}}}$$ は、当然ながら予測に必要な情報を保持する。しかし2,562個の場をすべて区別するため、圧縮を行わない。

逆に、極端に粗い観測は大幅な圧縮を実現できるが、一般には未来を区別できない。

したがって問題は、

> どこまで区別を捨てても、目的とする未来を失わないか

という形になる。

本研究の有限データ集合と一時刻先の場予測という条件のもとでは、その境界が692クラスとして具体的に求められた。

これは、

$${\text{compression}}$$

と

$${\text{predictive sufficiency}}$$

を別々の軸として扱う必要があることを示している。

粗い観測であること自体は十分ではない。また、予測可能であることだけなら恒等観測でも達成できる。

求めたいのは、**予測に必要な区別だけを残し、それ以外の区別を捨てること**である。

---

## 7.7 692は「発見されたマクロ変数」ではない

ただし、ここで重要な留保がある。

692クラスが得られたからといって、本研究がABCWの自然なマクロ変数を発見したとはまだ言えない。

第一に、この分割は観測された有限到達集合から構成されている。

第二に、予測対象は一時刻先の $${\Delta W}$$ に限定されている。

第三に、692クラスの構成は未来応答に基づくものであり、それぞれのクラスが単純な物理量やネットワーク量として表現できることは示されていない。

第四に、最小クラス数692は確定していても、それを実現する具体的なクラスラベルや表現方法が唯一であることまでは意味しない。

したがって、本結果から直接主張できるのは、

> 観測された有限ABCW力学において、一時刻先の行動条件付き場応答を完全に保存するために、2,562個のミクロな場の区別すべては必要ではなく、少なくとも692種類の予測上の区別が必要かつ十分である

ということである。

---

## 7.8 ミクロとマクロのあいだ

以上から、今回の692クラスは、ミクロな完全記述と単純なマクロ統計量の中間にある、**指定された未来に必要な区別だけを残した状態記述**として位置づけられる。

ただし、これをABCW一般の自然なマクロ変数とみなすことはできない。より大きな系、異なる初期条件、多時刻先予測での安定性や、692クラスを簡潔なネットワーク量で再表現できるかは未解決である。これらの意味と射程を次節で議論する。

---

# 8. Discussion

## 8.1 What the exact minimum means

本研究の中心的な問いは、

> **未来を予測するために、現在のどの区別を残す必要があるか。**

というものであった。

5主体ABCWの今回観測された有限到達集合では、2,562種類の異なる現在場 $${\Delta W}$$ が得られた。これらをすべて区別する恒等的なfield representationを用いれば、一時刻先の完全場 $${\Delta W_{t+1}}$$ を予測するための情報は失われない。しかし、本研究の問いは完全な現在場が予測に十分かどうかではなく、その区別のうちどこまでを捨てても指定された未来を失わないか、という点にある。

Sec. 6で得られた厳密な結果は、

$${|\operatorname{Im}B_{\min}|=\chi(G)=692}$$

であった。

したがって、今回の有限到達集合、field-only compression、現在行動 $${a_t}$$ の保持、一時刻先の完全場 $${\Delta W_{t+1}}$$ の100%予測という条件のもとでは、

$${2562\longrightarrow692}$$

まで現在場の区別を減らすことができる。一方、691クラス以下では、少なくとも一つの共通行動条件のもとで異なる次場を生成する現在場を同一視することになり、完全予測を保存できない。

この意味で692は、単なる圧縮アルゴリズムの出力ではない。また、任意に選んだ特徴量の性能を表す数でもない。今回指定した予測課題に対して、**残さなければならないfield distinctionの最小数**である。

ただし、この解釈には明確な限定が必要である。692はABCW一般の状態数でも、自然に存在する普遍的なマクロ状態数でもない。この値は、主体数、初期場、到達集合、観測形式、予測対象、時間幅、および100%予測を要求するという条件に依存する。

したがって、本研究の主結果の意味は「ABCWには692個のマクロ状態がある」ということではない。より限定的には、

> **今回の有限ABCW力学では、一時刻先の完全場を予測するために2,562個のミクロな場の区別すべてを保持する必要はないが、少なくとも692種類のfield distinctionは保持しなければならない**

ということである。

---

## 8.2 Microscopic difference and predictive relevance

この結果から得られる中心的な解釈は、

$${\text{ミクロに異なること}}$$

と

$${\text{指定された未来を予測するために区別する必要があること}}$$

が同じではない、という点である。

実際、最小692分割には352個のsingleton classが存在する一方、340クラスでは複数の異なる $${\Delta W}$$ が統合され、最大クラスには65種類の異なる現在場が含まれる。

したがって、完全に個別識別しなければならない場も多数存在するが、ミクロには異なるにもかかわらず、今回の予測目的に対しては同一視できる場も広範に存在する。

さらに、同じ予測クラスに入るかどうかは、$${\Delta W}$$ の成分差による単純な近さとは一致しない。比較的大きく異なる場が同一クラスに入りうる一方、互いに近い場であっても、ある共通行動条件のもとで異なる次場を生成すれば別クラスへ分離される。

したがって、最小分割が保存しているものは現在場の静的な形状そのものではなく、

$${\Delta W_t\longmapsto\left(a\longmapsto\Delta W_{t+1}\right)}$$

として表される、観測された**action-conditioned one-step future response**である。

この点は、状態記述の「細かさ」を、現在状態そのものの幾何学や成分数だけで評価することの限界を示している。

予測という目的を固定したとき、重要なのは二つの現在状態がどれほど似て見えるかではなく、それらの違いが目的とする未来の違いとして現れるかどうかである。

---

## 8.3 Hand-designed observables and dynamics-derived partitions

本研究では、最小分割を直接求める前に、ノルム、局所構造、out-strengthなど、人間があらかじめ選んだネットワーク特徴量による場の圧縮を検討した。

これらの特徴量は無意味ではない。とくにout-strengthは高い予測性能を示し、$${(a,\mathrm{out\mbox{-}strength})}$$ による11,142個の観測状態のうち11,084状態では次場が一意に定まり、状態単位決定率は99.4794%であった。

しかし、残る58個の衝突状態を解消しながら真に異なる $${\Delta W}$$ を統合する特徴量の組を探索した結果、検討した9特徴の非空部分集合511候補の範囲では、真のfield compressionと100%予測を同時に達成する候補は得られなかった。

この失敗だけを見れば、完全予測には現在場をほぼそのまま保持する必要があるようにも見える。

しかしSec. 6の結果はそうではないことを示す。

特徴量という事前制約を外し、どの現在場同士を同一視すると未来の衝突が生じるかを直接用いれば、2,562場は692クラスまで圧縮できる。

したがって、今回の結果では、

$${\text{人間に自然な特徴量}}$$

と

$${\text{予測に必要な最小区別}}$$

は一致しなかった。

ここから、「自然な特徴量は予測に不適切である」という一般的結論を導くことはできない。今回検査した特徴族は有限であり、別の特徴量やその構成によって692分割、あるいは別の高性能な圧縮を簡潔に表現できる可能性は残る。

むしろ本研究が示すのは、特徴量を先に仮定する方法とは別に、

$${\text{未来を保存するために必要な区別を力学から先に求める}}$$

という逆向きの方法が可能だということである。

その意味で692分割は、解釈可能なマクロ変数の最終回答というより、将来そのような表現を探索するときの**予測上の基準**として位置づける方が適切である。

---

## 8.4 Relation to state aggregation and predictive-state ideas

Sec. 2で整理したように、本研究の問題設定は、state aggregation、lumpability、bisimulation、computational mechanics、およびincompletely specified finite-state machine minimizationと複数の接点を持つ。

まずlumpabilityとの共通点は、ミクロ状態をまとめた後にも将来についてwell-definedな記述を残そうとする点にある。

ただし、本研究では

$${P(X_t)\longrightarrow P(X_{t+1})}$$

というself-closureと、

$${P(X_t)\longrightarrow Z}$$

という指定されたtarget predictionを区別した。

今回保存したのは縮約されたfield class自身の次状態ではなく、一時刻先の完全場 $${\Delta W_{t+1}}$$ である。したがって、692分割がそのまま閉じた縮約ダイナミクスを構成することは、本研究の結果からは従わない。

bisimulationやMDP minimizationとも、将来挙動に必要な区別によって状態をまとめるという発想を共有する。しかしABCWについて本研究が保存したのは最適方策、報酬構造、あるいは縮約モデル全体ではない。現在行動を保持し、field variableだけを圧縮したうえで、一時刻先の完全場を保存するという限定された問題である。

computational mechanicsにおけるcausal statesとは、「未来にとって必要な区別だけを残す」という問題意識がとくに近い。しかしcausal statesが過去を未来系列の条件付き確率分布によって分類するのに対し、本研究は有限到達集合上の現在場を対象とし、予測対象を一時刻先の完全場に限定している。また、今回のinput-output dataは部分指定されており、すべての現在場についてすべての行動条件が観測されているわけではない。

そのため、692クラスをcausal statesあるいはε-machineと呼ぶことはしない。

数学的により直接的な対応を持つのは、Sec. 2で述べたincompletely specified finite-state machine minimizationである。今回のデータは、

$${(\Delta W,a)\longmapsto\Delta W'}$$

という部分指定されたinput-output behaviorとして読める。同じ入力条件 $${a}$$ のもとで異なる出力 $${\Delta W'}$$ を生じる二つの現在場を同一クラスへ入れられないというcompatibility / incompatibilityの構造は、この古典的問題と直接対応する。

一方、本研究では後続クラスの再帰的整合性を要求せず、保存対象を一時刻先の完全場に限定した。このdepth-1という条件によって、最小field class数をincompatibility graphのchromatic numberとして直接求めることができた。

したがって、本研究の理論的位置づけは、既存のstate-minimizationやpredictive representationの一般理論を新たに提案するものではない。

本稿の具体的な貢献は、競合的な有限エージェント力学から得られた部分指定データについて、このdepth-1 predictive state-reduction problemを明示的に構成し、その最小値を上界構成と独立な下界によって厳密に確定した点にある。

---

## 8.5 The structure behind 692

692という最小値は、2,562場を一様に細かく分割した結果ではない。

Sec. 6の下界構成とSec. 7の内部構造解析では、単一のアンカー行動

$${a=(-,-,-,-,-)}$$

のもとで観測された1,239場が625種類の異なる次場を生成することから、まず625クラスが必要になる。

しかし、この625群を他の行動条件について検査すると、575群には追加の内部衝突がなく、50群だけに追加のincompatibilityが存在した。

この50群を厳密に分割すると117サブクラスが必要となり、

$${117-50=67}$$

だけクラス数が増加する。

したがって、

$${625+67=692}$$

である。

この構造は、予測に必要な区別がすべての現在場へ均等に分布しているわけではないことを示す。

大部分のアンカー群では、一つの行動条件から得られた区別だけで十分である。追加の行動条件によって新たな区別が必要になるのは50群に限られる。

したがって、今回の最小予測分割は、

$${\text{大きな基本分割}+\text{局所的な追加分解}}$$

として理解できる。

ただし、この局在性から直ちに一般的な「予測情報の局在則」を主張することはできない。ここで確認されたのは、今回の有限データ集合と予測課題において、625から692への追加区別が限定されたアンカー群に集中していたという事実である。

それでも、この構造は、最小分割を単なる692ラベルのlookup tableとして扱う場合には見えにくい。

どの条件が新しい区別を要求するのかを追うことで、最小クラス数だけでなく、**予測上重要な差異がどこで露出するか**を解析できることを示している。

---

## 8.6 Scope and limitations

本研究の結果には、少なくとも以下の限定がある。

第一に、解析対象は5主体ABCWであり、4種類の初期場から生成された今回の有限到達集合に限られる。したがって、692という値を異なる主体数、異なる初期条件、あるいはABCW一般へ外挿することはできない。

第二に、本研究では現在行動 $${a_t}$$ を観測に保持し、field variable $${\Delta W_t}$$ だけを圧縮した。したがって、行動と場を同時に圧縮する一般的な最小状態表現を求めたわけではない。

第三に、予測対象は一時刻先の完全場 $${\Delta W_{t+1}}$$ である。692分割が複数歩先予測でも十分であること、あるいは692クラス上に閉じた再帰的ダイナミクスが存在することは検証していない。

第四に、解析したinput-output behaviorは部分指定されている。すべての現在場についてすべての行動条件が観測されているわけではない。したがって、今回得られた最小値は観測された有限到達集合に対する厳密解であり、未観測の組合せに対する予測保証を意味しない。

第五に、本研究では100%のone-step predictionを制約として採用した。これは最小分割を厳密に定義するためには有効であるが、100%予測だけが科学的に有意味な目標であることを意味しない。実際、out-strengthのように完全予測には達しなくても高い予測性能を持つはるかに単純な表現が存在する。

第六に、692という最小クラス数が確定しても、そのクラスを簡潔なネットワーク特徴量、代数的規則、あるいは人間に解釈しやすい少数の変数で表現できることは示されていない。また、最小クラス数が692であることは、minimum coloringとしての具体的なpartitionが一意であることも意味しない。

これらの限定は、主結果を弱めるというより、その射程を定めるものである。

本研究で厳密に確定したのは、**指定された有限データ、観測形式、予測対象、時間幅のもとで必要十分な最小field class数**である。

---

## 8.7 Future directions

以上の限定から、いくつかの自然な拡張が生じる。

第一は、予測時間幅の拡張である。一時刻先では同一視できる二つの場が、複数時刻先では異なる未来を生じる可能性がある。逆に、予測対象を将来の完全場ではなく、より粗い量へ変更すれば、現在場を692よりさらに粗くまとめられる可能性もある。

第二は、exact predictionからapproximate predictionへの拡張である。本研究では100%予測を制約として最小クラス数を求めたが、実際のモデル分析では、予測性能、圧縮率、表現コストの間のトレードオフが重要になる。高い予測性能を持つ単純な特徴量と、100%予測を保証する692分割との間には、多数の中間的表現が存在しうる。

したがって、

$${\text{predictive performance}}$$

$${\text{compression}}$$

$${\text{representation cost}}$$

を別々の軸として扱い、そのPareto構造を調べることは一つの方向となる。

第三は、692分割の可読な表現を探すことである。今回の結果は、どの区別を残せば未来を失わないかを力学から逆算できることを示した。しかし、それを人間が理解しやすい少数のネットワーク量へ再表現できるかは未解決である。

第四は、主体数、初期場、到達集合を変えたときに最小予測分割がどのように変化するかを調べることである。これによって初めて、今回観測された構造のどこまでがABCWのより一般的な性質であり、どこまでが今回の有限データに固有なのかを比較できる。

これらは本稿の主結果には含めない。

本研究が確定したのは、より限定されたdepth-1 problemについてである。その限定によって、予測に必要な区別という抽象的な問いを、完全に検査可能な有限問題として解くことができた。

---


---

# 9. Conclusion

## 9.1 Main result

本研究では、5主体ABCWの有限到達集合を対象に、現在行動 $${a_t}$$ を保持したままfield $${\Delta W_t}$$ だけを圧縮し、一時刻先の完全場 $${\Delta W_{t+1}}$$ を100%一価に予測するために必要な最小field class数を求めた。

観測された2,562種類の現在場からincompatibility graphを構成し、692色のproper coloringによる上界と、アンカー行動から得られる独立な下界を一致させることで、

$${|\operatorname{Im}B_{\min}|=\chi(G)=692}$$

を厳密に確定した。したがって、今回の予測課題では2,562個のミクロな場の区別すべては必要ではない一方、691クラス以下のfield-only partitionでは完全予測を保存できない。

## 9.2 Interpretation and scope

この最小値は一様な分割から生じたものではない。アンカー行動のもとで625個の基本群が必要となり、そのうち50群だけが他の行動条件による追加分解を要求する。追加67クラスによって $${625+67=692}$$ となり、最終分割は352個のsingleton classと340個のmulti-field classから構成される。

また、9特徴族の511組合せを調べたnatural-feature baselineでは、out-strength vectorが99.4794%の状態単位決定率を示した一方、真のfield compressionと100%予測を同時に達成する候補は得られなかった。したがって今回の結果では、人間が事前に選ぶ自然な特徴量と、未来を保存するために必要な最小区別は一致しなかった。

ただし、692はABCW一般の普遍的なマクロ状態数ではない。この値は5主体、今回の有限到達集合、action保持、field-only compression、one-step exact-field predictionという条件に依存する。また、最小クラス数が692であることは、具体的なminimum coloringの一意性や、692クラスを簡潔な解析的観測写像で表現できることを意味しない。

## 9.3 Outlook

次の課題は、複数時刻先予測、近似予測を許した場合の圧縮とのtrade-off、主体数や初期場を変えた場合のスケーリング、および692分割をより少数の解釈可能な構造量で表現できるかを調べることである。

本稿の最も限定的な結論は、**状態として異なることと、指定された未来を予測するために区別する必要があることは同じではない**、という点にある。ABCWにおける692という最小予測分割は、「未来を失わずに現在をどこまで忘れてよいか」という問いを、具体的な有限力学上で厳密に解いた一例である。

---

# References

Arthur, W. B. (1994). Inductive reasoning and bounded rationality. *American Economic Review*, 84(2), 406–411.

Brélaz, D. (1979). New methods to color the vertices of a graph. *Communications of the ACM*, 22(4), 251–256. doi:10.1145/359094.359101

Bron, C., & Kerbosch, J. (1973). Algorithm 457: Finding all cliques of an undirected graph. *Communications of the ACM*, 16(9), 575–577. doi:10.1145/362342.362367

Challet, D., & Zhang, Y.-C. (1997). Emergence of cooperation and organization in an evolutionary game. *Physica A: Statistical Mechanics and its Applications*, 246(3–4), 407–418. doi:10.1016/S0378-4371(97)00419-6

Givan, R., Dean, T., & Greig, M. (2003). Equivalence notions and model minimization in Markov decision processes. *Artificial Intelligence*, 147(1–2), 163–223. doi:10.1016/S0004-3702(02)00376-4

Kemeny, J. G., & Snell, J. L. (1960). *Finite Markov Chains*. Van Nostrand.

Kohavi, Z., & Jha, N. K. (2009). *Switching and Finite Automata Theory* (3rd ed.). Cambridge University Press.

Paull, M. C., & Unger, S. H. (1959). Minimizing the number of states in incompletely specified sequential switching functions. *IRE Transactions on Electronic Computers*, EC-8(3), 356–367. doi:10.1109/TEC.1959.5222697

Shalizi, C. R., & Crutchfield, J. P. (2001). Computational mechanics: Pattern and prediction, structure and simplicity. *Journal of Statistical Physics*, 104(3–4), 817–879.

Tishby, N., Pereira, F. C., & Bialek, W. (2000). The information bottleneck method. arXiv:physics/0004057.
