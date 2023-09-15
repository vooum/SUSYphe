# Prospino2 说明文档

**作者：** 贾兴隆

Prospino2 是一个计算强子对撞机中 `MSSM` 超对称粒子(次)领头阶产生截面的 Fortran90 程序，目前常见的 Fortran 编译器例如 gcc, g++, gfortran 都可以对其进行编译。

## Prospino2 官方网站

<https://www.thphys.uni-heidelberg.de/~plehn/index.php?show=prospino>

## Prospino2 文件说明

该程序最重要的几个文件分别是

- 主程序文件 prospino_main.f90
- 可执行文件 prospino_2.run
- 输入文件 prospino.in.les_houches
- 输出文件 prospino.dat

如果需要立刻查看该程序包的运行方法，可直接跳转至可执行文件 `prospino_2.run` 的介绍章节。

### 主程序文件 prospino_main.f90

该文件包含了截面计算中最重要的某些参数设置，同时也是该程序包 `main` 函数所在的位置。每次修改该文件后都需要进行编译才能使更改生效。

这些参数依次是：

#### inlo

该部分指定将要计算的是截面是领头阶 (LO) 的还是次领头阶 (NLO) 的。

如果 `inlo = 0` 则计算 LO 截面，如果 `inlo = 1` 则计算 NLO 截面。

```fortran
!----------------------------------------------------------------------------
  inlo = 1       ! specify LO only[0] or complete NLO (slower)[1]           !
!                ! results: LO     - LO, degenerate squarks, decoupling on  !
!                !          NLO    - NLO, degenerate squarks, decoupling on !
!                !          LO_ms  - LO, free squark masses, decoupling off !
!                !          NLO_ms - NLO, free squark masses, scaled        !
!                ! all numerical errors (hopefully) better than 1%          !
!                ! follow Vegas iteration on screen to check                !
!----------------------------------------------------------------------------
```

这个代码的注释中还提到了输出结果的含义，这一点本文档会稍后提及

#### isq_ng_in

该部分指定 `squark` 质量是否是简并的。

如果 `isq_ng_in = 0` 则 `squark` 质量简并，如果 `isq_ng_in = 1` 则 `squark` 质量自由。如无特殊需求，该项应指定为 `isq_ng_in = 1`。

```fortran
!----------------------------------------------------------------------------
  isq_ng_in = 1     ! specify degenerate [0] or free [1] squark masses      !
                    ! [0] means Prospino2.0 with average squark masses      !
                    ! [0] invalidates isquark_in switch                     !
!----------------------------------------------------------------------------
```

#### icoll_in & energy_in

该部分指定强子对撞机的类型以及对撞能量。

如果 `icoll_in = 0` 则对撞机类型将指定为 `Tevatron`，如果 `icoll_in = 1` 则对撞机类型将指定为 `LHC`。

对撞能量 `energy_in` 需要手动指定，单位是 `GeV`。当前 `LHC` 的对撞能量为 13 TeV 即 13000 GeV

```fortran
!----------------------------------------------------------------------------
  icoll_in = 1      ! collider : tevatron[0], lhc[1]                        !
  energy_in = 13000 ! collider energy in GeV                                !
!----------------------------------------------------------------------------
```

#### i_error_in

该部分指定误差是否随能标改变。

如果 `i_error_in = 0` 则误差不随能标改变，如果 `i_error_in = 1` 则随能标改变。如无特殊情况，应设置为 `i_error_in = 0`。

```fortran
!----------------------------------------------------------------------------
  i_error_in = 0    ! with central scale [0] or scale variation [1]         !
!----------------------------------------------------------------------------
```

#### final_state_in

该部分指定所计算截面的末态产生模式。

常用的有 `final_state_in = nn` 即 `neutralino/chargino` 对儿产生模式，以及 `final_state_in = ll` 即 `slepton` 对儿产生模式。

```fortran
!----------------------------------------------------------------------------
  final_state_in = 'nn'                                                     !
!                                                                           !
!                   ng     neutralino/chargino + gluino                     !
!                   ns     neutralino/chargino + squark                     !
!                   nn     neutralino/chargino pair combinations            !
!                   ll     slepton pair combinations                        !
!                   sb     squark-antisquark                                !
!                   ss     squark-squark                                    !
!                   tb     stop-antistop                                    !
!                   bb     sbottom-antisbottom                              !
!                   gg     gluino pair                                      !
!                   sg     squark + gluino                                  !
!                   lq     leptoquark pairs (using stop1 mass)              !
!                   le     leptoquark plus lepton (using stop1 mass)        !
!                   hh     charged Higgs pairs (private code only!)         !
!                   ht     charged Higgs with top (private code only!)      !
!                                                                           !
!  squark and antisquark added, but taking into account different sb or ss  !
!----------------------------------------------------------------------------
```

#### ipart1_in & ipart2_in

该部分用于指定所计算截面的末态粒子具体类型，仅当末态产生模式被指定为 `ng, ns, nn, ll, tb, bb` 时生效。

以 `final_state_in = nn` 和 `final_state_in = ll` 两种模式为例：

当 `final_state_in = nn` 时，`ipart1_in` 和 `ipart2_in` 均指某一特定的 `neutralino/chargino`，分别是

- 指定为 1, 2, 3, 4 时对应 $\tilde{\chi}_{1,2,3,4}^0$
- 指定为 5, 6 时对应 $\tilde{\chi}_{1,2}^+$
- 指定为 7, 8 时对应 $\tilde{\chi}_{1,2}^-$

当 `final_state_in = ll` 时，`ipart2_in` 此时不生效，必须设置为 `ipart2_in = 1`，`ipart1_in` 对应特定的标轻子对儿产生，例如 `ipart1_in = 1` 时指左手标电子对儿产生，`ipart1_in = 2` 时指右手标电子对儿产生。剩余产生类型可具体查看代码内的注释。

```fortran
!----------------------------------------------------------------------------
  ipart1_in = 7                                                             !
  ipart2_in = 5                                                             !
!                                                                           !
!  final_state_in = ng,ns,nn                                                !
!  ipart1_in   = 1,2,3,4  neutralinos                                       !
!                5,6      positive charge charginos                         !
!                7,8      negative charge charginos                         !
!  ipart2_in the same                                                       !
!      chargino+ and chargino- different processes                          !
!                                                                           !
!  final_state_in = ll                                                      !
!  ipart1_in   = 0        sel,sel + ser,ser  (first generation)             !
!                1        sel,sel                                           !
!                2        ser,ser                                           !
!                3        snel,snel                                         !
!                4        sel+,snl                                          !
!                5        sel-,snl                                          !
!                6        stau1,stau1                                       !
!                7        stau2,stau2                                       !
!                8        stau1,stau2                                       !
!                9        sntau,sntau                                       !
!               10        stau1+,sntau                                      !
!               11        stau1-,sntau                                      !
!               12        stau2+,sntau                                      !
!               13        stau2-,sntau                                      !
!               14        H+,H- in Drell-Yan channel                        !
!                                                                           !
!  final_state_in = tb and bb                                               !
!  ipart1_in   = 1        stop1/sbottom1 pairs                              !
!                2        stop2/sbottom2 pairs                              !
!                                                                           !
!  note: otherwise ipart1_in,ipart2_in have to set to one if not used       !
!                                                                           !
!----------------------------------------------------------------------------
```

#### isquark1_in & isquark2_in

该部分用于指定所计算截面的末态粒子具体类型，仅当末态产生模式涉及轻味 `squark` 时生效。

```fortran
!----------------------------------------------------------------------------
  isquark1_in = 0                                                           !
  isquark2_in = 0                                                           !
!                                                                           !
!  for LO with light-squark flavor in the final state                       !
!  isquark1_in     =  -5,-4,-3,-2,-1,+1,+2,+3,+4,+5                         !
!                    (bL cL sL dL uL uR dR sR cR bR) in CteQ ordering       !
!  isquark1_in     = 0 sum over light-flavor squarks throughout             !
!                      (the squark mass in the data files is then averaged) !
!                                                                           !
!  flavors in initial state: only light-flavor partons, no bottoms          !
!                            bottom partons only for Higgs channels         !
!                                                                           !
!  flavors in final state: light-flavor quarks summed over five flavors     !
!                                                                           !
!----------------------------------------------------------------------------
```

#### 其余事项

该文件的其它内容均为 `main` 函数的语句，但该文件中有一部分注释可能需要注意：

```fortran
!----------------------------------------------------------------------------
!  input file: prospino.in.leshouches                                       !
!              use block MASS for masses, plus low-energy mixing matrices   !
!                                                                           !
!  output file: prospino.dat   for compact output format                    !
!               prospino.dat2  for long output including subchannels        !
!               prospino.dat3  lo file for masses, flags, etc               !
!----------------------------------------------------------------------------
```

该注释告诉用户，该程序的输入文件为 `prospino.in.leshouches`，输出文件为 `prospino.dat, prospino.dat2, prospino.dat3`。文档后面的章节会详细介绍这些内容。

### 可执行文件 prospino_2.run

每当 `prospino_main.f90` 中的配置信息发生修改时，都需要使用 `make` 命令进行编译才能使更改在可执行文件 `prospino_2.run` 中生效。

该文件的使用方法为直接执行，例如当位于该文件的同一级目录时，执行命令为 **`./prospino_2.run`**。

直接运行时会有很多信息打印在屏幕上，如果不希望这些信息被打印出来，则可以使用诸如 **`./prospino_2.run > a.txt`** 这样的命令，把输出信息存放在一个名为 `a.txt` 的文件中。
