import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）／画面内：True，画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate
def game_over(screen:pg.Surface) ->None:
    """
    ゲームオーバを表示させる関数
    引数：screenはpygeme 表示のSueface
    """
    #画面を黒く塗る
    black_img = pg.display.set_mode((WIDTH, HEIGHT))
    black_img.fill((0,0,0))  
    screen.blit(black_img,(0,0))
    #泣いている工科トン
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct_left = kk_img.get_rect()
    kk_rct_left.center = (WIDTH // 2)-200, HEIGHT // 2 
    screen.blit(kk_img, kk_rct_left)
    kk_rct_right = kk_img.get_rect()
    kk_rct_right.center = (WIDTH // 2)+200, HEIGHT // 2 
    screen.blit(kk_img, kk_rct_right)
    #テキスト作成
    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    text_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(txt, text_rect)
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    拡大する爆弾のSurfaceリストと加速度リストを作成する関数
    戻り値：爆弾リスト、加速度リスト
    """    
    bb_imgs=[]#爆弾リスト
    bb_acc=[]#加速度リスト
    for r in range(1,11):#半径10倍まで
        bb_img=pg.Surface((20 * r, 20 * r),pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
        bb_acc.append(r)
    return bb_imgs, bb_acc
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動した方向によって工科トンの画像をゲットする関数
    引数：sum_mvは合計の移動量タプル
    戻り値:対応している工科トンのSurface
    """
    kk_imgs = {
        (0, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (0, 5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    }
    return kk_imgs.get(sum_mv, pg.image.load("fig/3.png"))



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く

    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_acc=init_bb_imgs()#初期化する
    sum_mv = [0, 0]
    while True:
        #爆弾のサイズと速度を時間経過によってかわる
        index = min(tmr // 500, 9)#ｔｍｒが500ごとに変化する
        bb_img =bb_imgs[index]
        avx = vx * bb_acc[index]
        avy = vy * bb_acc[index]
        bb_rct.move_ip(avx, avy)#爆弾の移動
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):#工科トンが衝突したら実行
            game_over(screen)
            return 
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら，元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()