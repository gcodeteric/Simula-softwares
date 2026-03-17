# Guia Técnico Definitivo: Todos os Carros GT3 e GT4 do iRacing

O iRacing disponibiliza atualmente **11 carros GT3** e **6 carros GT4** ativos, cada um com características de condução, sensibilidades de setup e pontos fortes radicalmente distintos. Este guia analisa individualmente cada carro com base em dados oficiais dos manuais do iRacing (s100.iracing.com), guias da Coach Dave Academy, análises da Apex Racing Academy, VRS, SimRacingCockpit.gg e discussões da comunidade em OverTake.gg e Reddit r/iRacing. **Nota crítica**: toda a classe GT3 recebeu uma reformulação total de pneus, aerodinâmica e BoP na Season 3 2025 (junho 2025), e a classe GT4 sofreu reformulação equivalente na Season 4 2025 (setembro 2025) — todos os setups anteriores a estas datas estão obsoletos.

---

## BLOCO 3 — Carros GT3 Disponíveis no iRacing (Análise Individual)

A classe GT3 do iRacing é composta por 11 máquinas de três configurações de motor: **front-engine** (BMW, Mercedes, Ford, Aston Martin), **mid-engine** (Ferrari, Lamborghini, Audi, McLaren, Corvette, Acura) e **rear-engine** (Porsche). Cada layout dita fundamentalmente o comportamento dinâmico do carro. A reformulação massiva da Season 3 2025 — descrita pelo iRacing como "the largest set of updates and improvements to existing content we've ever shipped at one time" — introduziu um novo tire model com recuperação de grip após derrapagens, modelo aerodinâmico baseado em CFD com sensibilidade real ao ride height, e recalibração completa do BoP. Os pneus agora necessitam de **4-5 voltas para atingir temperatura ótima**, e os heat spikes já não destroem a performance para o resto do stint.

### BMW M4 GT3 EVO

**Especificações**: Motor inline-6 biturbo de 3.0L (derivado do S58 BMW), **~590 cv**, **644 Nm** de binário, **1.285 kg** de peso seco, tração traseira, caixa sequencial de 6 velocidades. Atualizado para especificação EVO na Season 4 2025 (atualização gratuita para proprietários existentes) com nova aerodinâmica, faróis e lanternas revistos. Na Season 1 2026, o engine model foi refinado para melhor corresponder às curvas de potência e engine braking fornecidas pela BMW.

**Perfil de comportamento**: O M4 GT3 é o carro GT3 **mais popular e versátil** da plataforma. Apresenta ligeiro understeer na entrada de curva (peso frontal típico de front-engine), mas é globalmente **equilibrado e previsível**. Na fase média da curva mantém uma plataforma estável, e na saída oferece tração excelente graças ao enorme binário disponível desde rotações médias. O motor turbo proporciona uma vantagem significativa em **circuitos de altitude** (Interlagos, México) onde motores aspirados perdem potência. A gestão de pneus é equilibrada quando conduzido corretamente. Classifica-se como o GT3 **mais amigável para iniciantes** segundo a Coach Dave Academy e SimRacingSetup.com.

**Pontos fortes**: Chassis grande que absorve bem curbs na entrada; sistema de traction control eficaz e pouco intrusivo; janela de setup ampla que permite configurações desde "pointy" até muito estáveis; entrega de potência turbo surpreendentemente linear; menos sensível a danos aerodinâmicos que carros mid-engine. **Pontos fracos**: Não tolera curbs agressivos na saída (exemplo: bus stop de Watkins Glen); downshifts prematuros causam instabilidade traseira; menos ágil e reativo que concorrentes mid-engine; resposta direcional mais lenta em chicanes rápidas.

**Parâmetros mais sensíveis**: O ângulo do rear wing e o ride height (ângulo de rake) devem ser ajustados em conjunto — aumentar +1 no wing requer -1.5 mm no front ride height ou +4.0 mm no rear ride height para manter o equilíbrio aerodinâmico. As anti-roll bars são a ferramenta principal para contrabalançar o understeer inerente. O diff preload controla transições on/off-throttle: aumentar preload suaviza transições mas pode causar snap oversteer com throttle agressivo. Os dampers (HS/LS compression e rebound) são críticos em pistas com irregularidades.

**Erros comuns de setup**: Fazer downshift demasiado cedo em curva (usar o binário e manter engrenagens altas); não ajustar rake ao alterar o rear wing; ser demasiado agressivo nos curbs; ignorar o ajuste de brake bias à medida que o combustível diminui durante o stint.

**Recomendações por tipo de circuito**: Em pistas de **high downforce** (Spa, Bathurst), aumentar rear wing com mais rake e front ARB ligeiramente mais rígida para rotação. Em pistas de **low downforce** (Monza, Daytona), reduzir wing e rake, priorizar velocidade em reta. Em **circuitos de rua** (Long Beach), wing médio, dampers mais suaves para absorver irregularidades, TC mais alto.

**Fontes de setups**: Coach Dave Academy (Delta subscription), GO Setups (gosetups.gg), Track Titan (app.tracktitan.io), iRacing baseline setups (significativamente melhorados após S3 2025).

### Porsche 911 GT3 R (992)

**Especificações**: Motor flat-six boxer aspirado de 4.2L (aumentado relativamente ao 4.0L do predecessor), **~565 cv**, **1.250 kg**, motor traseiro, tração traseira, caixa sequencial de 6 velocidades. Classificação oficial do iRacing: "Clubman" — designação enganadora, dado que a comunidade o considera o GT3 **mais difícil de dominar**.

**Perfil de comportamento**: O 992 é o GT3 mais singular do iRacing. O motor traseiro cria uma dinâmica de pêndulo única: **understeer pronunciado em curvas de média e alta velocidade** (o peso traseiro impede a rotação frontal) mas **tração de saída excepcional** — "All that rear weight plants the tyres under acceleration. I get on the power earlier in this thing than the BMW or the Ferrari" (SimRacingCockpit.gg). O perigo reside no **snap oversteer sem aviso** quando qualquer input brusco excita a massa traseira. A filosofia de condução é "slow in, fast out" — travar cedo, rodar o carro pacientemente, e explorar a tração devastadora na saída. Em stints avançados, os snaps tornam-se mais difíceis de corrigir à medida que os pneus degradam.

**Pontos fortes**: Melhor tração de saída em curvas lentas de todos os GT3; estabilidade excecional em travagem em linha reta; setup de referência do iRacing classificado "top 3" na classe GT3 (SimRacingCockpit.gg); teto de performance altíssimo quando dominado. **Pontos fracos**: Understeer severo em curvas rápidas; snap oversteer repentino e irrecuperável; cada input de pedal e volante desloca a massa traseira; performance comprometida em circuitos de alta velocidade (Spa, Monza); piso de habilidade mais elevado de qualquer GT3.

**Parâmetros mais sensíveis**: As ARBs são o instrumento primário — front mais rígida + rear mais suave cria rotação para compensar o understeer inerente, mas em incrementos mínimos (um click de cada vez). Os spring rates seguem a mesma lógica: front mais rígido, rear mais suave. O **aero balance** é extremamente sensível — mudanças minúsculas têm efeitos desproporcionais. Tire pressures target: **1.50-1.55 bar** a quente; pressões mais altas causam instabilidade traseira a meio do stint.

**Erros comuns**: Sobrecorrigir o aero balance (mudanças pequenas têm efeitos enormes); pressões de pneu demasiado altas; fazer múltiplas alterações de setup simultaneamente em vez de uma mudança por teste; tentar forçar o carro em curvas rápidas em vez de respeitar as suas limitações.

**Recomendações**: Em circuitos técnicos e lentos (Barber, Long Beach), o carro brilha naturalmente — mais aero frontal, springs traseiros suaves. Em circuitos rápidos (Spa, Monza), aceitar o compromisso em curvas de alta velocidade e focar na tração de saída. Em circuitos de rua, configurações intermédias focadas nas zonas de tração.

**Fontes**: Coach Dave Academy, SimRacingCockpit.gg (guia detalhado gratuito), Track Titan, iRacing baseline setup.

### Ferrari 296 GT3

**Especificações**: Motor V6 biturbo de 3.0L (Ferrari F163), **~600 cv** (pré-BoP), **664 Nm**, **1.350 kg** (seco), **1.508 kg** (com piloto e fluidos), mid-engine, tração traseira, caixa sequencial de 6 velocidades. Wheelbase de 2.660 mm. Gera **20% mais downforce** que o predecessor 488 GT3 Evo. Adicionado ao iRacing na Season 4 2023.

**Perfil de comportamento**: A Ferrari 296 é o GT3 mid-engine de referência — descrito pela Coach Dave Academy como "adaptable, forgiving for the newbie and challenging enough for the seasoned sim racing expert." O setup de referência apresenta algum understeer na entrada e oversteer na saída com aplicação agressiva de throttle. É mais neutro que o 488 Evo e não sofre da sensibilidade de pitch do Porsche. A técnica de condução recomendada: "Aim for 90-95% peak brake pressure and bleed off smoothly as you turn. Straighten the wheel before squeezing power" (iRacerHub). Os pneus traseiros são o indicador-chave — temperaturas traseiras elevadas no F9 box indicam demasiado wheelspin ou yaw.

**Pontos fortes**: Layout mid-engine com distribuição de peso superior; 20% mais downforce que o predecessor; setup de referência competitivo imediatamente; disponível em séries dedicadas (Ferrari GT3 Challenge classe D, Ferrari Rain Master); recomendado como um dos três melhores GT3 para iniciantes. **Pontos fracos**: Afinação de setup mais complexa que o 488 Evo — trade-offs específicos por pista; oversteer na saída com throttle agressivo; sobreaquecimento de pneus traseiros se não gerido; "unforgiving if you rush your inputs" (iRacerHub).

**Parâmetros mais sensíveis**: O diff preload é o parâmetro mais impactante — aumentar preload cria mais understeer off-throttle e mais snap oversteer com throttle agressivo, mas suaviza transições. O aero balance (front splitter + rear wing) tem impacto significativo dado o elevado downforce do carro. As tire pressures devem começar baixas e subir gradualmente. O low speed compression damping controla a velocidade de transferência de peso.

**Erros comuns**: Aplicação de throttle demasiado agressiva na saída (provoca picos de temperatura nos pneus traseiros); não dosear os travões suavemente na entrada (ativa ABS de forma oscilatória); demasiadas alterações de setup simultâneas; demasiado diff preload causando snap oversteer imprevisível.

**Recomendações**: High downforce (Spa, Bathurst): mais rear wing, gestão cuidadosa da saída de curva. Low downforce (Monza, Daytona): reduzir wing, aproveitar motor turbo em retas. Circuitos de rua: aero intermédio, foco na gestão de temperaturas dos pneus.

**Fontes**: Coach Dave Academy, iRacing manual oficial (s100.iracing.com/wp-content/uploads/2024/06/Ferrari-296-GT3-V4.pdf), iRacerHub, Apex Racing Academy BoP analysis.

### Mercedes-AMG GT3 2020

**Especificações**: Motor V8 aspirado AMG de 6.3L (6.2L real) DOHC, **550 cv**, **1.285 kg**, front-mid engine com transaxle traseiro para melhor distribuição de peso, tração traseira, caixa sequencial de 6 velocidades. Capacidade de combustível: 105.99 litros. Classificação iRacing: Advanced. Na Season 1 2026, o ride height tornou-se diretamente ajustável (anteriormente exigia alteração dos spring perch offsets).

**Perfil de comportamento**: O Mercedes é simultaneamente understeery E oversteery dependendo da fase da curva — um perfil complexo que exige condução metódica. Na entrada tende a ser loose (peso frontal carrega rapidamente sob travagem); no mid-corner oferece forte grip frontal quando bem configurado; na saída, a potência massiva do V8 aspirado sobrecarrega facilmente os pneus traseiros com o mínimo de intervenção do TC. "Even small moments of oversteer can result in huge losses of lap time" (Coach Dave Academy). O traseiro leve requer gestão constante.

**Pontos fortes**: Capacidade de absorção de curbs **superior a qualquer outro GT3** — "takes curbs like no other" (Coach Dave Academy); resiliente a contactos menores e danos aerodinâmicos; potência V8 aspirado suave e massiva sem turbo lag; boa escolha para condutores metódicos e consistentes. **Pontos fracos**: Traseiro leve difícil de gerir (oversteer na entrada E na saída); consumo de combustível elevado; velocidade de ponta inferior a alguns rivais; TC minimamente intrusivo (menos proteção que o BMW); apenas disponível a partir da licença C.

**Parâmetros mais sensíveis**: Front springs/ARBs/dampers devem ser mais rígidos para estabilizar a plataforma frontal e gerir a transferência de peso. O rear wing deve ser mantido relativamente alto para colar o traseiro ao asfalto. O front splitter é a ferramenta primária de afinação do aero balance — mais splitter encoraja oversteer. O brake bias mais recuado melhora rotação na entrada.

**Erros comuns**: Não rigidificar suficientemente o front end; rear wing demasiado baixo (expõe o traseiro leve); inputs agressivos de travão e throttle; ignorar gestão de consumo de combustível em endurance; virar demasiado tarde — deve-se virar CEDO e induzir mais rotação.

**Recomendações**: High downforce: mais rear wing e front splitter; o Mercedes adora configurações de high downforce. Low downforce: compromisso necessário — reduzir wing expõe o traseiro. Circuitos de rua: explorar a vantagem nos curbs; gerir combustível em corridas longas.

**Fontes**: Coach Dave Academy, iRacing manual (s100.iracing.com/wp-content/uploads/2024/07/Mercedes-AMG-GT3-2020-Manual_V9.pdf), SimRacingSetup.com, GO Setups.

### McLaren 720S GT3 EVO

**Especificações**: Motor V8 biturbo de 4.0L (M840T), **~700 cv** (pré-BoP), mid-engine, tração traseira, caixa sequencial de 6 velocidades, chassis em fibra de carbono MonoCage II. Adicionado ao iRacing na Season 4 2024, substituindo o McLaren MP4-12C GT3.

**Perfil de comportamento**: A versão EVO foi redesenhada para ser **mais neutra** que o 720S original, com equilíbrio aerodinâmico deslocado para a frente. O carácter geral é neutro a ligeiramente rotation-happy. Na entrada pode ser snappy se a travagem não estiver completa antes do turn-in — a transferência de peso do layout mid-engine causa snap oversteer com trail braking demasiado agressivo. No mid-corner oferece boa rotação. Na saída, o binário twin-turbo pode causar perda de tração mais facilmente que carros aspirados. Excelente estabilidade a alta velocidade.

**Pontos fortes**: Estabilidade a alta velocidade e equilíbrio aerodinâmico consistente; boa rotação em curvas de média/alta velocidade; equilíbrio neutro acessível para pilotos intermédios; forte em ar limpo. **Pontos fracos**: Pode ser snappy em curvas lentas; turbo lag torna a gestão de tração mais complexa que carros aspirados; menos eficaz sobre curbs que carros front-engine; suscetível a mudanças repentinas de equilíbrio.

**Parâmetros mais sensíveis**: O aero balance deve ser mantido próximo de 50% — abaixo de 50% cria mais rotação a alta velocidade, acima de 50% mais estabilidade. Front/rear aero matching deve ser simétrico para evitar drag e equilíbrio imprevisível. Rear ARBs/springs: suavizar para reduzir oversteer. Diff preload: aumentar para suavizar transições on/off-throttle.

**Erros comuns**: Aero balance demasiado longe de 50%; rear suspension demasiado rígida causando snap oversteer; atacar curbs agressivamente; TC/ABS demasiado elevados em seco.

**Fontes**: Coach Dave Academy, iRacing manual (s100.iracing.com/wp-content/uploads/2024/09/Mclaren-720S-GT3_V2.pdf), GO Setups, SimRacingSetup.

### Lamborghini Huracán GT3 EVO

**Especificações**: Motor V10 aspirado de 5.2L, **~500 cv** (BoP), **~545 Nm**, **1.285 kg** (seco), mid-engine, tração traseira (o carro de estrada é AWD; regulamento GT3 impõe RWD), caixa sequencial de 6 velocidades. Wheelbase: 2.645 mm. Nota: continua na especificação EVO 1, não EVO2.

**Perfil de comportamento**: Inerentemente **bem equilibrado** devido à distribuição de peso próxima de 50-50 do layout mid-engine. Boa rotação inicial na entrada, responsivo a trail braking mas não tão snappy quanto o McLaren. No mid-corner é excelente — grip e estabilidade para levar velocidade enorme em curvas de média/alta velocidade. Na saída, o V10 aspirado proporciona resposta de throttle imediata e linear sem qualquer turbo lag. Surpreendentemente estável sobre curbs para um carro mid-engine.

**Pontos fortes**: Distribuição de peso 50-50 perfeita; resposta de throttle imediata (V10 aspirado); capacidade de cornering excecional ("its greatest strength"); boa gestão de pneus; estabilidade aerodinâmica a alta velocidade. **Pontos fracos**: Sem a vantagem de tração traseira do Porsche; não tão agressivo nos curbs como carros front-engine; velocidade em reta não é a melhor; natureza implacável quando o equilíbrio está errado.

**Parâmetros mais sensíveis**: Ride height + splitter adjustment são críticos para equilíbrio aerodinâmico e mecânico. Anti-roll bars são a ferramenta primária para equilíbrio understeer/oversteer. TC e ABS (range 1-10, baseline fabricante 3-4, ótimo em iRacing tipicamente 3-6). Spring rates mais suaves em pistas com irregularidades.

**Erros comuns**: Ignorar o requisito de equilíbrio 50-50; TC demasiado alto matando velocidade de saída; alterações múltiplas em vez de incrementais; não adaptar o estilo de condução ao mid-engine.

**Fontes**: Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-lamborghini-huracan-gt3-evo/), SimRacingSetup, GO Setups.

### Audi R8 LMS GT3 EVO II

**Especificações**: Motor V10 aspirado de 5.2L, **585 cv**, **550+ Nm**, **~1.235 kg** (seco, mais leve que o predecessor), mid-engine, tração traseira, caixa sequencial pneumática de 6 velocidades. Dampers Penske 4-way (LSC, HSC, LSR, HSR). Adicionado ao iRacing na Season 1 2024.

**Perfil de comportamento**: Muito responsivo com excelente grip geral, mas pode apresentar snap oversteer se o piloto não for cuidadoso. Boa rotação natural na entrada — superior a outros mid-engine — mas pode saltar com release de travão abrupto. O V10 aspirado proporciona resposta de throttle excelente, PORÉM o sistema de TC é bastante intrusivo, frequentemente necessitando de coasting antes da aceleração total, mesmo com TC baixo. A nova asa traseira gera mais downforce traseiro que o predecessor.

**Pontos fortes**: Grip geral excelente; V10 aspirado = resposta imediata; mais leve que o predecessor com mais potência; dampers 4-way ajustáveis permitem afinação detalhada; rotação natural torna-o ágil. **Pontos fracos**: Snap oversteer com release de travão descuidado; TC intrusivo mesmo em settings baixos; requer técnica de coasting; mais exigente e peaky que alguns rivais.

**Parâmetros mais sensíveis**: "The majority of your work needs to be done with ride height and splitter adjustments" (Coach Dave Academy). O diff preload é "crucial setup tool for this car to control rotation and acceleration." TC e ABS (range 1-10, fabricante recomenda 3-4). Rear toe-in: aumenta estabilidade mas valores excessivos criam drag.

**Erros comuns**: Confiar excessivamente nos dampers em vez de focar primeiro no ride height/splitter; TC demasiado baixo sem adaptar técnica de condução; não monitorar a leitura de aero balance no menu de setup; alterações de toe demasiado grandes.

**Fontes**: Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-audi-r8-lms-evo-ii-gt3/), GO Setups, Track Titan.

### Ford Mustang GT3

**Especificações**: Motor V8 Coyote aspirado de 5.4L, **~516 cv** (BoP), **~1.315 kg**, front-engine (posicionado atrás do eixo dianteiro), tração traseira, caixa sequencial de 6 velocidades. Construído em colaboração Ford/Multimatic Motorsports, baseado no 2024 Mustang Dark Horse. Adicionado na Season 3 2024.

**Perfil de comportamento**: "Very stable and friendly on track, great for those new to GT3 racing" (Coach Dave Academy). Comportamento semelhante ao BMW M4 e ao Mercedes. Understeer na entrada quando trava forte para curvas, mas gerível. Plantado em curvas lentas e médias. Excelente sobre curbs — "stable and smooth over kerbs, barely moving and maintaining its line well." Na saída, entra bem em curvas lentas quando sai dos travões. Boa velocidade de ponta.

**Pontos fortes**: Amigável para iniciantes — competitivo com setup de referência; absorção de curbs excecional; V8 aspirado = entrega de potência previsível; all-rounder versátil; recomendado pela Coach Dave como top 3 GT3 para iniciantes (com BMW e Ferrari). **Pontos fracos**: Sente-se "big and heavy"; menos ágil que mid-engine; trail braking a alta velocidade pode causar numbness frontal seguida de snap traseiro; posição de condução baixa com dashboard alto pode exigir ajuste.

**Parâmetros mais sensíveis**: O rear wing angle é o ajuste aerodinâmico primário (sem front splitter ajustável). Cada +1 de wing requer compensação de ride height (-1.5 mm frente ou +4.0 mm atrás). As anti-roll bars são a ferramenta mecânica de equilíbrio principal. Brake bias para gerir understeer na entrada.

**Erros comuns**: Conduzir em excesso na entrada (causando understeer ou snap a alta velocidade); não ajustar ride heights ao alterar wing; ignorar ajuste de posição do piloto; tentar conduzi-lo como um carro mid-engine.

**Fontes**: Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-ford-mustang-gt3/), iRacing manual (s100.iracing.com/wp-content/uploads/2024/06/Mustang-GT3_Manual_V2.pdf), GO Setups.

### Chevrolet Corvette Z06 GT3.R

**Especificações**: Motor V8 flat-plane crank aspirado de 5.5L (baseado no LT6), **520 cv**, **583 Nm**, **1.335 kg** (seco), mid-engine, tração traseira, caixa Xtrac sequencial de 6 velocidades com **4 gear stacks** disponíveis (IMSA, FIA, Le Mans, Daytona). Dampers Penske 4-way. Adicionado na Season 3 2024.

**Perfil de comportamento**: Classificado pela Coach Dave Academy na categoria mid-engine junto com Ferrari 296 e Lamborghini. Boa rotação natural no turn-in sem necessidade de forçar. O default setup produz um traseiro **ligeiramente mais solto que o Ferrari 296** em curvas lentas. Satisfatório de manobrar em curvas lentas. Na saída pode sofrer de **slow-speed oversteer** — facilita ativação do TC que corta potência. O motor aspirado flat-plane proporciona curva de binário linear. "A true joy to drive" (BoxThisLap). Descrito como "fun and agile" com "precise cornering and exceptional stability at high speeds."

**Pontos fortes**: Motor aspirado com binário linear; equilíbrio mid-engine natural; boa rotação no mid-corner; som único de flat-plane V8; 4 opções de gear stack por circuito; disponível em 9 séries; "fast becoming a fan-favourite" (Coach Dave Academy). **Pontos fracos**: Oversteer em curvas lentas com setup default; menos estável sobre curbs que front-engine; TC ativa facilmente em baixa velocidade; ligeiramente mais pesado que alguns rivais; dependência de setup aerodinâmico.

**Parâmetros mais sensíveis**: Ride heights extremamente sensíveis — targets dinâmicos ótimos: frente 37.5 mm (±2.5 mm), traseiro 57.5 mm (±2.5 mm). Sair destas janelas causa perda rápida de downforce. O rear wing (range +0.5 a +9.5) requer compensação de ride height. Rear spring rate e rear ARB são as ferramentas primárias para o oversteer em baixa velocidade. O diff (friction faces + preload) controla comportamento off-throttle e on-throttle.

**Erros comuns**: Ride heights fora das janelas ótimas; não compensar ride heights ao alterar wing; suavizar excessivamente para corrigir oversteer (piora estabilidade aerodinâmica); TC demasiado alto (o motor aspirado permite TC mais baixo); rake excessivo (o manual indica que o Corvette "will perform best with a relatively low-rake setup").

**Recomendações por circuito** (do manual oficial): High downforce (Brands Hatch, Sebring, Long Beach): wing +9.5, gear stack IMSA. Medium (Spa, Monza, Le Mans): wing intermédio, gear stack FIA/Le Mans. Low downforce (Daytona): wing mínimo, gear stack Daytona.

**Fontes**: iRacing manual oficial, Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-chevrolet-corvette-z06-gt3-r/), BoxThisLap.

### Acura NSX GT3 EVO 22

**Especificações**: Motor V6 biturbo de 3.5L, **~520 cv**, mid-engine, tração traseira, caixa semi-automática sequencial de 6 velocidades. Wheelbase ~40 mm mais curto que o McLaren 720S GT3. Primeiro carro GT3 japonês adicionado ao iRacing. Adicionado na Season 1 2025.

**Perfil de comportamento**: Posiciona-se na extremidade "pointy" dos GT3 mid-engine — mais agressivo que o Ferrari 296 ou o Lamborghini. O setup base é understeery, mas quando corrigido, o carro pode tornar-se rotation-happy e difícil de manter consistente. O wheelbase mais curto torna-o mais snappy. O V6 biturbo sofre de **turbo lag**, tornando a gestão de tração mais complexa que carros aspirados. O destaque absoluto são os **travões excelentes** — "allowing you to brake later than most other GT3s without drama" — vantagem decisiva em circuitos de travagem pesada (Monza, Red Bull Ring).

**Pontos fortes**: Capacidade de travagem superior — ponto de travagem mais tardio de toda a classe GT3; boa agilidade mid-engine; suspensão Evo 22 redesenhada mais fácil que predecessores; configurações múltiplas de faróis úteis para endurance. **Pontos fracos**: Turbo lag complica aplicação de throttle; wheelbase curto = mais snappy e difícil de ser consistente; mais sensível a curbs que rivais; encontrar equilíbrio de setup correto é crítico.

**Parâmetros mais sensíveis**: Aero balance (splitter + rear wing) deve ser mantido simétrico. Spring rates suaves ajudam em pistas irregulares. Anti-roll bars são a ferramenta principal de transição understeer/oversteer. TC é especialmente importante dado o turbo lag.

**Erros comuns**: Eliminar demasiado understeer criando um carro instável; chassis demasiado rígido em pistas irregulares; uso agressivo de curbs; saltar para o throttle cedo demais (turbo lag → perda súbita de tração).

**Fontes**: Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-the-honda-nsx-gt3-evo/), iRacing manual (s100.iracing.com/wp-content/uploads/2024/12/Acura-GT3_Manual_V2.pdf).

### Aston Martin Vantage GT3 EVO

**Especificações**: Motor V8 biturbo de 4.0L DOHC (derivado do Mercedes-AMG), **~600 cv** (pré-BoP), **~1.330 kg**, front-engine com gearbox transaxle traseiro, tração traseira, caixa sequencial de 6 velocidades. Quick-adjust rear wing ajustável na pit stop. Adicionado na Season 4 2025, o mais recente GT3 na plataforma.

**Perfil de comportamento**: "Stable, planted and forgiving" com toque de understeer típico de front-engine. Sensação similar ao Mercedes-AMG GT3 (partilham família de motor). Na entrada pode sentir-se "floaty" sem trail braking, com oversteer ocasional sob travagem pesada. No mid-corner é mais equilibrado que o Vantage GT3 original. Na saída, atenção ao wheelspin — pode virar para oversteer com throttle ganancioso. Excelente sobre curbs graças ao layout front-engine.

**Pontos fortes**: Plataforma estável e previsível; absorção de curbs agressiva; som fantástico (V8 AMG partilhado); aerodinâmica EVO melhorada; "new content in iRacing is likely to be strong in the meta for its first season"; transição fácil para quem já conduz o Mercedes GT3. **Pontos fracos**: Menos ágil que mid-engine; understeer inerente de front-engine; sensação floaty no turn-in sem trail braking; muito recente — setups e conhecimento da comunidade ainda em desenvolvimento.

**Parâmetros mais sensíveis**: Rear wing (quick-adjust); ride heights (sensíveis ao modelo aero pós-S3 2025); anti-roll bars; brake bias; spring rates.

**Erros comuns**: Não fazer trail braking (causa turn-in flutuante); throttle demasiado ganancioso na saída; suavizar a frente excessivamente; usar setups do Aston Martin GT3 antigo (carro completamente diferente).

**Fontes**: Coach Dave Academy (coachdaveacademy.com/tutorials/iracing-guide-new-aston-martin-vantage-gt3-evo/), iRacing manual (s100.iracing.com/wp-content/uploads/2026/01/Aston-Martin-GT3-Evo-V1.pdf).

### Tabela comparativa resumo — GT3

| Carro | Facilidade de Setup | Amigável p/ Iniciantes | Competitividade (BoP) | Dificuldade Gestão Pneus | Melhores Circuitos |
|---|---|---|---|---|---|
| BMW M4 GT3 EVO | ★★★★★ | ★★★★★ | Alta (constante) | Baixa | Todos; brilha em altitude |
| Porsche 911 GT3 R (992) | ★★☆☆☆ | ★★☆☆☆ | Alta (quando dominado) | Alta (traseiros) | Técnicos/lentos |
| Ferrari 296 GT3 | ★★★★☆ | ★★★★☆ | Alta (consistente) | Média (traseiros) | Todos; versátil |
| Mercedes-AMG GT3 2020 | ★★★☆☆ | ★★★☆☆ | Alta (track-dependent) | Média (frontais) | High downforce; curbs |
| McLaren 720S GT3 EVO | ★★★☆☆ | ★★★☆☆ | Alta (teto alto) | Média | High speed; técnicos |
| Lamborghini Huracán GT3 EVO | ★★★★☆ | ★★★☆☆ | Média-Alta | Baixa | Todos; cornering |
| Audi R8 LMS GT3 EVO II | ★★★☆☆ | ★★★☆☆ | Média-Alta | Média | Todos; técnicos |
| Ford Mustang GT3 | ★★★★★ | ★★★★★ | Alta (recente) | Baixa | Todos; curbs |
| Corvette Z06 GT3.R | ★★★☆☆ | ★★★☆☆ | Média-Alta | Média | Técnicos; mid-speed |
| Acura NSX GT3 EVO 22 | ★★★☆☆ | ★★☆☆☆ | Média | Média-Alta | Travagem pesada |
| Aston Martin Vantage GT3 EVO | ★★★★☆ | ★★★★☆ | Alta (novo, BoP favorável) | Média | Curbs; estabilidade |

**Notas sobre BoP recentes**: A Apex Racing Academy publicou análises semanais de BoP que indicam que a **Ferrari 296, Mercedes AMG e Ford Mustang GT3** são consistentemente Tier 1 ou 2. O **BMW M4 GT3 EVO** e o **Porsche 992** são fortes mas track-dependent. O Aston Martin Vantage GT3 EVO beneficia tipicamente de BoP favorável enquanto conteúdo novo. A BoP é ajustada **semanalmente** por pista nas séries GT Sprint e IMSA — nenhum carro domina consistentemente em todas as pistas.

---

## BLOCO 4 — Carros GT4 Disponíveis no iRacing (Análise Individual)

A classe GT4 do iRacing sofreu uma **reformulação completa de físicas, pneus e performance** na Season 4 2025 (setembro 2025). O novo tire model exige um período de aquecimento, o peso e potência base foram aumentados para correlacionar com o regulamento real IMSA Michelin Pilot Challenge, as velocidades de ponta subiram e as velocidades mínimas de curva diminuíram. Todos os setups anteriores a esta atualização estão invalidados. A classe compõe-se de **4 carros front-engine** e **2 carros mid-engine**, todos RWD com caixa sequencial.

### Mercedes-AMG GT4

**Especificações**: Motor V8 biturbo de 4.0L (front-mounted), **544 cv** (declarado pelo iRacing), **~1.500 kg** (BoP), front-mid engine, tração traseira, caixa DCT de 7 velocidades (operação sequencial). Eletrónica: TC, ABS, ESC ajustáveis.

**Perfil de comportamento**: Understeer ligeiro, especialmente na entrada e mid-corner (típico front-engine GT4). Muito estável globalmente. Fases mais fortes: saída de curva (binário massivo), curbs (excelente compostura), travagem (superior à maioria dos rivais). Fase mais fraca: rotação no mid-corner — o grande V8 frontal reduz agilidade. Estabilidade a alta velocidade excelente graças ao wheelbase longo e peso frontal. Desgaste de pneus relativamente uniforme e previsível.

**Pontos fortes**: **GT4 mais popular do iRacing e melhor all-rounder** — recomendado pela Coach Dave Academy como escolha #1; equilíbrio perdoador excelente para iniciantes E com ritmo para pilotos experientes; absorve curbs com facilidade; boa velocidade em reta; capacidade de travagem forte. **Pontos fracos**: Não tão ágil como mid-engine (Porsche, McLaren); problemas de rotação no mid-corner; understeer pode ser frustrante em séries fixed setup.

**Parâmetros mais sensíveis**: **Front toe** negativo elevado (~-1.8°) é crítico para combater understeer. Camber -3.5° ou inferior em ambos os eixos. Front spring rates suaves (~150 N/mm) para melhorar grip. Rear ARB mais rígida que a dianteira para rotação. Dampers: rigidificar bump e rebound 3-4 clicks acima de suave para gerir saltos sobre curbs.

**Erros comuns**: Não usar front toe negativo suficiente; front springs demasiado rígidas (understeer crónico); não compensar springs suaves com dampers mais rígidos (causa bouncing); rear ARB demasiado suave relativamente à dianteira.

**Recomendações**: High downforce: mais rear wing, foco em aero balance via ride heights/rake. Low downforce (Daytona, Monza): reduzir wing, minimizar drag. Técnicos/rua: suspensão frontal suave, toe negativo alto, maximizar grip mecânico.

**Fontes**: Coach Dave Academy Mercedes GT4 Guide, iRacing manual (s100.iracing.com/wp-content/uploads/2024/07/Mercedes-AMG-GT4-Manual-V2.pdf).

### Porsche 718 Cayman GT4 Clubsport MR

**Especificações**: Motor flat-6 aspirado de 3.8L (mid-rear mounted), **425 cv**, **~1.495 kg**, mid-engine, tração traseira, caixa PDK de 6 velocidades (operação sequencial). TC, ABS, ESC ajustáveis.

**Perfil de comportamento**: Understeer na entrada e travagem (peso traseiro reduz grip frontal), mas pode virar para oversteer se pressionado em excesso ou desestabilizado por curbs. Fases mais fortes: mid-corner (ágil, responsivo) e tração na saída (layout mid-engine). Fase mais fraca: sobre curbs (mid-engine = mais sensível) e travagem (understeer por falta de peso frontal). Muito ágil em curvas lentas — leva mais velocidade que rivais front-engine. Os pneus frontais podem desgastar-se mais rápido se levar velocidade excessiva na entrada.

**Pontos fortes**: Handling ágil e responsivo; performance excecional no mid-corner; tração excelente na saída; divertido de conduzir; excelente stepping stone do MX-5 Cup para GT3; menos punitivo que o Porsche 992 GT3 R. **Pontos fracos**: Sensível a curbs agressivos; understeer na entrada requer técnica de travagem cuidadosa; necessita estilo de condução suave; pune a condução excessiva.

**Parâmetros mais sensíveis**: Front ARB — reduzir blade settings para distribuir carga e reduzir understeer. Front toe-out para induzir rotação e melhorar turn-in. Brake bias — mover 1-2% para trás do default para melhorar rotação traseira sob travagem. Spring rates front-to-rear cruciais. Higher negative front camber para grip no mid-corner.

**Erros comuns**: Velocidade excessiva na entrada causando understeer severo; excesso de steering angle (sobrecarrega frontais); brake bias insuficientemente recuado; suspensão frontal demasiado rígida.

**Recomendações**: Circuitos técnicos e sinuosos: terreno natural do carro — maximizar grip mecânico, suspensão suave, mais toe-out. Circuitos rápidos: ainda competitivo mas requer gestão cuidadosa. Circuitos com curbs pesados: suspensão suave e dampers afinados.

**Fontes**: Coach Dave Academy Porsche 718 GT4 Guide, iRacing manual (s100.iracing.com/wp-content/uploads/2024/07/Porsche-718-Cayman-GT4-Manual-V5.pdf).

### BMW M4 G82 GT4 EVO

**Especificações**: Motor inline-6 biturbo de 3.0L (front-mounted), **~530 cv**, **~1.500 kg**, front-engine, tração traseira, caixa DCT de 7 velocidades. Travões: 6 pistões à frente, 4 atrás. Substitui o F82 GT4 desde a Season 4 2024. Na Season 4 2025 Patch 3 recebeu: "BoP: reduced aero drag and moved CoP rearward."

**Perfil de comportamento**: Understeer ligeiro a moderado (front-engine); pode sentir-se lento em mudanças de direção. Fases mais fortes: velocidade em reta (**a mais rápida de todos os GT4**), estabilidade, absorção de curbs. Fase mais fraca: mudanças rápidas de direção (chicanes), rotação no mid-corner. Estabilidade a alta velocidade excelente. Previsível mas não o mais ágil.

**Pontos fortes**: **Maior velocidade de ponta de qualquer GT4** — crucial em corridas; handling previsível; bom sobre curbs; excelente para iniciantes; aerodinâmica melhorada da versão G82 EVO. **Pontos fracos**: Sensação sluggish (front-engine); rotação pobre em chicanes; understeer na entrada pode ser persistente; não tão ágil como mid-engine.

**Parâmetros mais sensíveis**: Front toe negativo alto essencial para turn-in. Front springs suaves para grip. Rake elevado para mais grip frontal no turn-in. Camber negativo alto em ambos os eixos. Rear wing tem efeito limitado no cornering no GT4 — mais útil para redução de drag.

**Erros comuns**: Rake insuficiente; compensar understeer suavizando excessivamente o traseiro (causa instabilidade); não explorar a vantagem de velocidade em reta na estratégia de corrida; esquecer que rear wing tem impacto mínimo no cornering em GT4.

**Recomendações**: Pistas de potência (Monza, Daytona): território natural — wing baixo, explorar vantagem de top speed. Técnicos: maximizar grip mecânico com toe alto, frente suave, rear ARB rígida. Rua: foco em compliance de curbs e paciência.

**Fontes**: Coach Dave Academy BMW M4 G82 GT4 Guide, iRacing manual (s100.iracing.com/wp-content/uploads/2024/12/BMW-M4-G82-GT4-Manual-V2.pdf).

### McLaren 570S GT4

**Especificações**: Motor V8 biturbo de 3.8L M838TE (mid-mounted), **~450 cv**, **355 lb-ft**, **~1.425 kg** (seco), **~1.540 kg** (com piloto), mid-engine, tração traseira, caixa SSG sequencial de 7 velocidades. Chassis: fibra de carbono MonoCell II com subframes de alumínio. Eletrónica: ABS/TC/ESC combinados com 3 modos (Normal/Sport/Track — Track recomendado). Pneus Pirelli: 265/645 frente, 305/680 traseiro. Apenas 2 posições de ARB (soft/stiff).

**Perfil de comportamento**: Equilibrado, posiciona-se entre understeer e oversteer. Pode empurrar (understeer) depois do apex mas é geralmente bem equilibrado. Fases mais fortes: travagem (forte e reativa), rotação no mid-corner, mudanças de direção. Fase mais fraca: pós-apex/saída (pode empurrar); curbs agressivos (sensibilidade mid-engine). Chassis de fibra de carbono proporciona rigidez excelente.

**Pontos fortes**: Handling middle-ground equilibrado; travagem excelente; mais ágil que carros front-engine; boa velocidade de ponta para mid-engine; all-rounder competitivo. **Pontos fracos**: Dificuldade com curbs agressivos; understeer pós-apex pode custar velocidade de saída; pode ser snappier que front-engine se pressionado; apenas 2 settings de ARB (soft/stiff) — range limitado.

**Parâmetros mais sensíveis**: ARB settings (apenas 2 posições cada — front stiff = mais understeer, rear stiff = mais oversteer). Rear wing setting (range significativo, ótimo 3-5 para maioria das pistas). Ride heights críticos para equilíbrio mecânico e aero. Spring rates devem corresponder ao carácter da pista. Dampers: bump stiffness 0-18. Brake pad compound: Low/Medium/High friction.

**Erros comuns**: Não ajustar rake ao alterar rear wing; springs demasiado rígidas em pistas irregulares; ignorar a relação entre mudanças de spring rate e ride height; usar modo ESC "Normal" em vez de "Track".

**Recomendações**: Técnicos: wing 3-5, springs suaves, priorizar grip mecânico. Potência: wing baixo, minimizar drag, maximizar velocidade em reta. Endurance: 100% fuel, wing 3-5 (do manual de referência iRacing).

**Fontes**: iRacing McLaren 570S GT4 Manual oficial V2, Coach Dave Academy GT4 comparison.

### Aston Martin Vantage GT4

**Especificações**: Motor V8 biturbo de 4.0L (front-mounted, mesma família do Mercedes-AMG GT4), **~400+ cv** (BoP), **~1.500 kg**, front-engine, tração traseira, caixa sequencial de 7 velocidades. TC e ABS ajustáveis. Na Season 4 2025 Patch 3 recebeu: "brake cooling increased, front splitter height reduced, BoP: aero drag reduced slightly."

**Perfil de comportamento**: Understeer ligeiro (front-engine) mas com mais rotação natural que outros GT4 front-engine graças ao wheelbase mais curto. Fases mais fortes: **travagem** (atributo mais destacado segundo Coach Dave — "one of the best in class"), absorção de curbs, velocidade em reta. Fase mais fraca: estabilidade traseira em baixa velocidade (traseiro difícil), mid-corner (pode understeer e perder tempo com velocidade de entrada excessiva). A alta velocidade é estável. O desgaste dos pneus frontais pode ser exacerbado pela tendência de understeer.

**Pontos fortes**: **Melhor travagem da classe GT4**; boa velocidade em reta; absorve curbs bem; mais rotação natural que esperado para o layout; entrega de potência twin-turbo suave. **Pontos fracos**: **Considerado o GT4 menos competitivo globalmente** (Coach Dave Academy); traseiro difícil em baixa velocidade; understeer na entrada; desgaste dos frontais; jack of all trades, master of none.

**Parâmetros mais sensíveis**: Brake bias (para frente = estabilidade, para trás = rotação no turn-in). Front ARB/springs: suavizar reduz understeer. Rear ARB: rigidificar melhora rotação. Ride heights/rake. Dampers para gerir resposta a curbs.

**Erros comuns**: Velocidade de entrada excessiva (agrava understeer); não maximizar a vantagem de travagem (melhor atributo do carro); não gerir desgaste dos frontais em endurance.

**Fontes**: Coach Dave Academy Aston Martin GT4 Guide, iRacing manual (s100.iracing.com/wp-content/uploads/2025/03/Aston-Vantage-GT4-Manual_V4.pdf).

### Ford Mustang GT4

**Especificações**: Motor V8 Coyote aspirado de 5.0L (front-mounted, **maior motor da classe GT4**), **~mid-400s a mid-500s cv** (BoP), **~1.450 kg**, front-engine, tração traseira, caixa sequencial de 6 velocidades. Velocidade máxima até 250 km/h. Dampers Multimatic DSSV. Painéis em fibra natural. Adicionado na Season 4 2025.

**Perfil de comportamento**: Understeer — **um dos GT4 mais estáveis e understeering**. Ainda mais dócil que o Mercedes-AMG GT4. Fases mais fortes: velocidade em reta (entre as melhores da classe), curbs (excelente — "barely flinches"), consistência em stints longos. Fases mais fracas: mudanças de direção (sluggish), agilidade em curvas (empurra), travagem (estável mas não a mais eficaz). O V8 aspirado de grande cilindrada proporciona resposta de throttle imediata sem turbo lag, mas o binário castiga os pneus traseiros se o throttle não for suave.

**Pontos fortes**: **Possivelmente o GT4 mais acessível do iRacing** — perfeito para iniciantes (9.5/10 para casual sim racers segundo Coach Dave); velocidade de ponta entre as melhores da classe; absorção de curbs excecional; previsível e consistente; V8 aspirado = resposta imediata. **Pontos fracos**: Understeer crónico; V8 com binário elevado causa wheelspin se não for suave no throttle; não ágil em mudanças de direção; travagem não tão eficaz como rivais (Mercedes); opções de aero limitadas (apenas rear spoiler ajustável, sem ajuste de front splitter).

**Parâmetros mais sensíveis**: Roll bars e suspensão são a ferramenta primária de equilíbrio. Brake bias é o ajuste in-car mais impactante. Rear wing angle principalmente para redução de drag. Springs e dampers devem ser afinados por pista.

**Erros comuns**: Combater understeer com mais ângulo de volante em vez de ajustar setup mecânico; throttle pesado (queima traseiros); levar velocidade excessiva para curvas; não usar brake bias ativamente.

**Recomendações**: Pistas de potência (Daytona, Monza, Spa): melhores circuitos do carro — wing baixo, explorar top speed V8. Técnicos: cautela com mudanças de direção, grip mecânico, frente suave. Rua: absorção de curbs excelente; paciência com o nariz compensa.

**Fontes**: Coach Dave Academy Ford Mustang GT4 Guide (publicado setembro 2025), iRacing.com car page.

### Análise comparativa entre GT4

**Mais fáceis de configurar**: O **Ford Mustang GT4** é o mais previsível com menos variáveis aerodinâmicas; o **Mercedes-AMG GT4** tem os padrões de setup mais bem documentados com enorme conhecimento da comunidade; o **BMW M4 G82 GT4 EVO** tem uma abordagem de setup front-engine straightforward.

**Maior margem de desenvolvimento (range de setup)**: O **McLaren 570S GT4** com o chassis de fibra de carbono e gama ampla de springs/dampers/wing oferece o maior range de ajuste. O **Mercedes-AMG GT4** responde bem a alterações mecânicas detalhadas. O **BMW M4 GT4** oferece boa amplitude em rake, springs e dampers.

**Comportamentos mais específicos/difíceis**: O **Porsche 718 Cayman GT4** exige estilo de condução suave e pune overdriving, com understeer na entrada que pode virar para oversteer. O **McLaren 570S GT4** tem sensibilidade mid-engine sobre curbs e pode ser snappy. O **Aston Martin Vantage GT4** tem um traseiro difícil em baixa velocidade.

**Mais competitivos atualmente**: Após a reformulação da S4 2025, a BoP é "pretty well balanced" segundo BoxThisLap. O **Mercedes-AMG GT4** é amplamente considerado o melhor performer global e mais popular. O **BMW M4 G82 GT4 EVO** é competitivo em pistas de potência com a melhor velocidade de ponta. O **Aston Martin Vantage GT4** é considerado relativamente o mais fraco.

**Melhores para iniciantes**: **Ford Mustang GT4** (9.5/10 Coach Dave) → **Mercedes-AMG GT4** (perdoador, suporte comunitário enorme) → **BMW M4 GT4** (previsível, acessível) → **Porsche 718 Cayman GT4** (recomendado como "perfect step up from MX-5 Cup" mas requer condução mais cuidadosa).

### Tabela comparativa resumo — GT4

| Carro | Facilidade de Setup | Amigável p/ Iniciantes | Competitividade (BoP) | Margem Desenvolvimento | Melhores Circuitos |
|---|---|---|---|---|---|
| Mercedes-AMG GT4 | ★★★★★ | ★★★★★ | ★★★★★ (melhor overall) | ★★★★☆ | Todos; high speed |
| BMW M4 G82 GT4 EVO | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | Potência/retas |
| Ford Mustang GT4 | ★★★★★ | ★★★★★ | ★★★★☆ (novo, BoP recente) | ★★★☆☆ | Potência; curbs |
| McLaren 570S GT4 | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ (maior range) | Técnicos; travagem |
| Porsche 718 Cayman GT4 | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ | Técnicos/sinuosos |
| Aston Martin Vantage GT4 | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ (mais fraco) | ★★★☆☆ | Travagem; retas |

### Princípios universais de setup GT4 (pós-S4 2025)

O grip mecânico domina na classe GT4 — estes carros produzem downforce mínimo comparado com GT3. O rear wing tem impacto limitado no cornering e serve principalmente para redução de drag em pistas de potência vs. ganhos mínimos de estabilidade em pistas rápidas. O novo tire model requer fase de aquecimento — cautela nos outlaps. O **front toe-out é a correção universal para understeer** na maioria dos GT4 front-engine. A combinação **front springs suaves + rear ARB rígida** é a abordagem mais comum para melhorar rotação em carros front-engine. O **brake bias é o ajuste in-car mais impactante**: para frente para estabilidade, para trás para rotação. O cross weight deve manter-se em **50.0%** para pistas de road course. Os ride heights afetam tanto o equilíbrio mecânico como aerodinâmico e devem ser reajustados sempre que os springs são alterados.

### Fontes globais de setups (ambas as classes)

Os principais fornecedores de setups em 2026 — Coach Dave Academy (Delta, ~£7.99/mês), VRS (€9.99/mês), GO Setups, SimRacingSetup, Grid-and-Go (especialista endurance), Track Titan — empregam todos pilotos com **10.000+ iRating**. A diferenciação já não está nos setups em si mas nas **ferramentas de coaching e telemetria**. Para opções gratuitas: iRacing baseline setups (atualizados por season), Majors Garage (majorsgarage.com), e community-shared setups nos fóruns do iRacing e Reddit r/iRacing. Canais YouTube recomendados para walkthroughs: Driver61, Jardier, Dave Cam, Dan Suzuki. A Apex Racing Academy publica análises semanais de BoP gratuitas (apexracingac.com) que são referência para a comunidade.