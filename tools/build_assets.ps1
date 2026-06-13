# 『雨の終わりに』Ren'Py版 画像アセット生成パイプライン
# ChatGPT(Chrome)で生成し Downloads\ame-assets-raw に置いた素材を、
#  ・背景 bg_*_raw.png        -> 1280x720 に縮小
#  ・立ち絵 bust_*_raw.png     -> 白背景を境界フラッドフィルで透過し、余白トリミング後 高さ680に縮小
# して game/images/ に書き出す。
# 使い方: powershell -ExecutionPolicy Bypass -File build_assets.ps1
# （RAW素材が無い場合はスキップ。RAWはサイズが大きいのでリポジトリには含めていない）

$RAW = Join-Path $env:USERPROFILE 'Downloads\ame-assets-raw'
$DST = Join-Path $PSScriptRoot '..\renpy\AmeNoOwariNi\game\images'
$DST = [System.IO.Path]::GetFullPath($DST)

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Collections.Generic;
public class AmeAssets {
  // simple resize (for backgrounds)
  public static void Resize(string inPath, string outPath, int w, int h) {
    using (Bitmap src = new Bitmap(inPath))
    using (Bitmap bmp = new Bitmap(w, h, PixelFormat.Format32bppArgb)) {
      using (Graphics g = Graphics.FromImage(bmp)) {
        g.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic;
        g.DrawImage(src, 0, 0, w, h);
      }
      bmp.Save(outPath, ImageFormat.Png);
    }
  }
  // flood-fill white bg to alpha from borders, trim, then scale to height (for character busts)
  public static string KeyBust(string inPath, string outPath, int thresh, int targetH) {
    Bitmap src = new Bitmap(inPath);
    int w = src.Width, h = src.Height;
    Bitmap bmp = new Bitmap(w, h, PixelFormat.Format32bppArgb);
    using (Graphics g = Graphics.FromImage(bmp)) { g.DrawImage(src, 0, 0, w, h); }
    src.Dispose();
    BitmapData bd = bmp.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
    int stride = bd.Stride; byte[] buf = new byte[stride*h];
    Marshal.Copy(bd.Scan0, buf, 0, buf.Length);
    bool[] rem = new bool[w*h]; Stack<int> st = new Stack<int>();
    Action<int,int> push = (x,y) => {
      if (x<0||y<0||x>=w||y>=h) return; int idx = y*w+x; if (rem[idx]) return;
      int o = y*stride + x*4; int b=buf[o], gg=buf[o+1], r=buf[o+2];
      int mn = b; if(gg<mn)mn=gg; if(r<mn)mn=r;
      if (mn >= thresh) { rem[idx]=true; st.Push(idx); } };
    for (int x=0;x<w;x++){ push(x,0); push(x,h-1);}
    for (int y=0;y<h;y++){ push(0,y); push(w-1,y);}
    while (st.Count>0){ int idx=st.Pop(); int x=idx%w, y=idx/w; push(x-1,y);push(x+1,y);push(x,y-1);push(x,y+1);}
    int minx=w,miny=h,maxx=-1,maxy=-1;
    for (int y=0;y<h;y++) for (int x=0;x<w;x++){
      int idx=y*w+x; int o=y*stride+x*4;
      if (rem[idx]) { buf[o+3]=0; continue; }
      int b=buf[o], gg=buf[o+1], r=buf[o+2]; int mn=b; if(gg<mn)mn=gg; if(r<mn)mn=r;
      if (mn>=thresh-26) { bool edge=false;
        if(x>0&&rem[idx-1])edge=true; else if(x<w-1&&rem[idx+1])edge=true;
        else if(y>0&&rem[idx-w])edge=true; else if(y<h-1&&rem[idx+w])edge=true;
        if(edge){ int a=(int)(255.0*(thresh-mn)/26.0); if(a<0)a=0; if(a>255)a=255; buf[o+3]=(byte)(255-a); } }
      if (buf[o+3] > 16) { if(x<minx)minx=x; if(x>maxx)maxx=x; if(y<miny)miny=y; if(y>maxy)maxy=y; } }
    Marshal.Copy(buf, 0, bd.Scan0, buf.Length); bmp.UnlockBits(bd);
    if (maxx<minx) { minx=0;miny=0;maxx=w-1;maxy=h-1; }
    int pad=8; minx=Math.Max(0,minx-pad); miny=Math.Max(0,miny-pad); maxx=Math.Min(w-1,maxx+pad); maxy=Math.Min(h-1,maxy+pad);
    int cw=maxx-minx+1, ch=maxy-miny+1;
    Bitmap crop = bmp.Clone(new Rectangle(minx,miny,cw,ch), PixelFormat.Format32bppArgb); bmp.Dispose();
    int newW=(int)Math.Round(cw*(double)targetH/ch);
    Bitmap outb = new Bitmap(newW, targetH, PixelFormat.Format32bppArgb);
    using (Graphics g=Graphics.FromImage(outb)){ g.InterpolationMode=System.Drawing.Drawing2D.InterpolationMode.HighQualityBicubic; g.DrawImage(crop,0,0,newW,targetH); }
    crop.Dispose(); outb.Save(outPath, ImageFormat.Png); outb.Dispose();
    return newW+"x"+targetH; }
}
"@ -ReferencedAssemblies System.Drawing

if (-not (Test-Path $RAW)) { Write-Host "RAW folder not found: $RAW (skip)"; return }

foreach ($s in 'title','shosai','ima','dai') {
  $in = Join-Path $RAW "bg_${s}_raw.png"
  if (Test-Path $in) { [AmeAssets]::Resize($in, (Join-Path $DST "bg_$s.png"), 1280, 720); Write-Host "bg_$s.png 1280x720" }
}
foreach ($c in 'kumai','kayoko','tabuchi','mizuhara') {
  $in = Join-Path $RAW "bust_${c}_raw.png"
  if (Test-Path $in) { $r=[AmeAssets]::KeyBust($in, (Join-Path $DST "bust_$c.png"), 236, 680); Write-Host "bust_$c.png $r" }
}
Write-Host "done -> $DST"
