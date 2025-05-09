lst=(
'00_NSE Straight tube','01_NSE Tee tube','02_NSE Both receiving reducer',
'03_NSE 90Bent tube','04_NSE 45Bent tube','05_NSE 22Bent tube','06_NSE 11_1/4Bent tube',
'07_NSE 5_5/8Bent tube','08_NSE 45Two-track tube','09_NSE 22_1/2Two-track tube',
'10_NSE T-shaped pipe with shallow buried Flange','11_NSE Short tube with socket',
'12_NSE Collar','13_NSE Cap','14_NSE Retainer gland','15_Straight tube no socket',
'16_NSE N-Link','17_NSE Liner'
)

FC_type={
'00':'直管','01': '二受T字管','02':'両受片落管','03':'曲管_90','04':'曲管_45','05':'曲管_22_1/2','06':'曲管_11_1/4',
'07':'曲管_5_5/8','08':'両受曲管_45','09':'両受曲管_22','10':'浅層埋設形フランジ付きT字管','11':'受挿し短管',
'12':'継輪','13':'帽','14':'押輪','15':'直管(ソケットなし)','16':'N-Link','17':'ライナー'
}

#直管-------------------------------------------------------------------------------------------------------------------------
strp=['075','100','150']

#二受T字管----------------------------------------------------------------------------------------------------
trct2=['075x075','100x075','100x100','150x075','150x100','150x150']

#受挿し片落ち管/挿し受片落ち管--------------------------------------------------------------------------------------
trct3=['100x075','150x100']

#浅層埋設形フランジ付きT字管--------------------------------------------------------------------------------------
trct4=['075x075','100x075','150x075']


#フランジ付きT字管----------------------------------------------------------------------------------------------------------------------
ttf=['075x075','100x075','150x075']

#受口直管075～150-------------------------------------------------------------------------------------------------------------------
#         d0,    ｄ5,    ｄ2,    Y,    P,      L(有効長), L3(継輪),ライナー
rcvd={
'075':(   75,   156.1,     93,  45,  199.5,  4000,     550,     74),
'100':(  100,   184.1,    118,  45,  199.5,  4000,     550,     74),
'150':(  150,   239.0,    169,  60,  238.0,  5000,     600,     99)
}

#受口異形管075～150-------------------------------------------------------------------------------------------------------------------
#                                                              押輪        N-Link
#         d0,    ｄ5,   ｄ2,     P,   d4,  E,  k,   □L,  L(継輪),  M,   L1,  B
rcvd1={
'075':(   75,   197,   93.0,   39,  159, 19, 18,  152,    18,   19,  32,   52),
'100':(  100,   232,  118.0,   39,  186, 23, 19,  178,    20,   20,  33,   53),
'150':(  150,   296,  169.0,   39,  250, 23, 20,    0,    20,   21,  38,   57)
}

#受口 継輪　帽------------------------------------------------------------------------------------------------------
#         d0,   ｄ5,    ｄ2,     P,    d4,     E,   k,       L(継輪), y1(胴付寸法), T1,      □L
rcvdk={
'075':(   75,   197,   93.0,   39,  159,     19,  18,      440,     185,        18.0,    152),
'100':(  100,   232,  118.0,   39,  186,     23,  19,      450,     190,        18.0,    178),
'150':(  150,   296,  169.0,   39,  250,     23,  20,      490,     235,        18.0,      0)
}

#二受T字管-------------------------
#          H,    I,      J,    L
trcts2={
'075x075':(120,  100,    290,  410),
'100x075':(120,  110,    290,  410),
'100x100':(140,  110,    310,  450),
'150x075':(140,  155,    290,  430),
'150x100':(160,  155,    310,  470),
'150x150':(190,  160,    310,  500)
}

#受挿し片落ち管/挿し受片落ち管----------------------------
#          A,    B,    C,   E,    L1,      L2
trcts3={
'100x075':(0,    0,    0,   0,    180,       0),
'150x100':(0,    0,    0,   0,    180,       0)
}
#曲管-------------------------------------------------
#        R,   L1,   L2
elbows_90={
'075':(  70,  100,  290,90),
'100':(  95,  130,  310,90),
'150':( 145,  180,  380,90)
}
elbows_45={
'075':(  70,   60,  250,45),
'100':(  95,   70,  260,45),
'150':( 145,  100,  290,45)
}
elbows_22={
'075':(  70,   50,  230,22.5),
'100':(  95,   50,  240,22.5),
'150':( 145,   70,  260,22.5)
}
elbows_11={
'075':(   70,  40,  230,11.25),
'100':(   95,  40,  230,11.25),
'150':(  145,  50,  250,11.25)
}
elbows_5={
'075':(  70,   40,  230,5.625),
'100':(  95,   40,  230,5.625),
'150':( 145,   40,  240,5.625)
}
#両受曲管
#        R,   L1
two_t_45={
'075':(  70,   60,  0,45),
'100':(  95,   70,  0,45),
'150':( 145,  100,  0,45)
}

two_t_22={
'075':(  70,   50,  0,22.5),
'100':(  95,   50,  0,22.5),
'150':( 145,   70,  0,22.5)
}

#フランジ-----------------------------------------------------
#        d0,   d2,   d3,   d4,   d5,   K,   m,   n,  L2'
flngs={
'075':(    75,     93,   125,  168,  211,  21,  3,   4,  26,   3000,     8.5, 11,  110,  80,19),
'100':(   100,    118,   152,  195,  238,  21,  3,   4,  26,   3000,     8.5, 11,  150,  90,19),
'150':(   150,    169,   204,  247,  290,  22,  3,   6,  26,   4000,     9.0, 12,  230, 106,19),
}

#浅層埋設形フランジ付きT字管------------------------------------------------
#          H,    I,    J,    L
sttfs={
'075x075':(160,  105,  290,  450),
'100x075':(160,  120,  290,  450),
'150x075':(160,  170,  290,  450),
}

#短管 帽------------------------------------------------
#        L1,    L2,   M,   M0,   LL
tnkns={
'075':(  240,   0,   55,  17,   92),
'100':(  240,   0,   55,  17,   93),
'150':(  285,   0,   55,  17,   94),
}

#押輪------------------------------------------------
#        d3,    d4,   d5,   E,   M,    n
rtngs={
'075':(   97,  159,   197,  19,   15,  4),
'100':(  122,  186,   232,  23,   16,  4),
'150':(  173,  241,   287,  23,   17,  6),
}