import sys, os, subprocess, urllib2, platform
from os.path import expanduser
import zipfile
import os.path



EAPNum = "27"  
MPSWin = """http://download-ln.jetbrains.com/mps/31/MPS-3.1-EAP1-"""+EAPNum+""".exe"""
MPSMac = """http://download-ln.jetbrains.com/mps/31/MPS-3.1-EAP1-"""+EAPNum+"""-macos.dmg"""
MPSLin = """http://download-ln.jetbrains.com/mps/31/MPS-3.1-EAP1-"""+EAPNum+""".tar.gz"""
MPSZip = """http://download-ln.jetbrains.com/mps/31/MPS-3.1-EAP1-"""+EAPNum+""".zip"""

MPSArcDir = """MPS 3.1 EAP"""

MPSDir = None

MbeddrDir = None

MbeddrRepo = """https://github.com/mbeddr/mbeddr.core.git"""

Debug = False



MPS_VMOPTIONS="""-client
-Xss1024k
-ea
-Xmx2100m
-XX:MaxPermSize=2256m
-XX:NewSize=512m
-XX:+HeapDumpOnOutOfMemoryError
-Dfile.encoding=UTF-8
-Dapple.awt.graphics.UseQuartz=true
-Didea.paths.selector=MPS30"""


def checkJavaVersion(java):
  vals = java.split() 
  a = [s for s in vals if "1.6" in s]
  b = [s for s in vals if "1.7" in s]
  c = [s for s in vals if "HotSpot" in s]
  if len(c) > 0:
    if len(a) + len(b) > 0:
      return True;
  return "Java version is not recognized";
  
  
def checkJava():  
  try:
    java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
    return checkJavaVersion(java)
  except OSError:
    return "No Java installed, please install Java 7"

def prepareDestDir():
  home = os.path.join(expanduser("~"), "mbeddr")
  print("Where would you like to install it["+home+"]: ")
  destdir = str(raw_input()).strip()
  if (destdir is None) or (len(destdir) == 0):
    print("Selecting " + home)
    destdir = home;
    
  try:
    if(not os.path.exists(destdir)):
      os.makedirs(destdir)
  except OSError:
    return False;
  
  return destdir;

def downloadFile(url, destdir):
  file_name = url.split('/')[-1]
  u = urllib2.urlopen(url)
  resName = os.path.join(destdir, file_name)
  f = open(resName, 'wb')
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  print "Downloading: %s Bytes: %s" % (file_name, file_size)

  file_size_dl = 0
  block_sz = 8192
  while True:
      buffer = u.read(block_sz)
      if not buffer:
	  break

      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,

  f.close()
  
  return resName
    
def getOs():
  s = platform.platform()
  if "Lin" in s:
    return "Lin"
  if "Mac" in s:
    return "Mac"
  if "Win" in s:
    return "Win"
  
def fakeDownload(url, dest):
  print "Would download ", url
  downloadFile("""http://www.kontextfrei.net/wp-content/themes/it-passau/rotator/sample-1.jpg""", dest);
  
#def downloadMPS_OS_Dep(dest):
#  url=None
#  s = getOs();
#  if "Lin" in s:
#    url=MPSLin
#  if "Mac" in s:
#    url=MPSMac
#  if "Win" in s:
#    url=MPSWin  
#  if Debug:
#    fakeDownload(url, dest);
#  else:
#    downloadFile(url, dest);

def downloadMPS(dest):
  url=MPSZip
  if Debug:
    fakeDownload(url, dest);
    return "/home/zaur/mbeddr/MPS-3.1-EAP1-27.zip"
  else:
    return downloadFile(url, dest);

    
def unzip(zipzip, dest):
  zfile = zipfile.ZipFile(zipzip)
  for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    zfile.extract(name, os.path.join(dest,dirname))

def cloneMbeddr(dest):
  MbeddrDir = os.path.join(dest, "mbeddr.github");
  if not os.path.exists(MbeddrDir):
    os.makedirs(MbeddrDir);
  os.system("git clone " + MbeddrRepo+ " " + MbeddrDir);
  print "Checking out fortissStable branch..."
  os.system("git --git-dir="+ os.path.join(MbeddrDir, ".git") + " checkout fortissStable");
  
def main():
  print("Welcome!")
  print("You are about to install the last stable version of mbeddr.")

  print "Detecting Java"  
  j = checkJava()
  if j != True:
    print j;
    return 1;  
  
  print "Detecting ant"
#TODO 
  print "NOT IMPLEMENTED"

  
  print "Preparing destination directory";  
  dest = prepareDestDir();
  if dest == False:
    print "Problem creating destination directory";
    return 1;
  
  print "Downloading MPS..."
  archive = downloadMPS(dest);
  
  
  print "Extracting..."
  unzip(archive, dest);
  

  print "Deleting archive"
  os.remove(archive);
  
  print "Renaming MPS folder"
  MPSDir = os.path.join(dest, "MPS31");
  os.rename(os.path.join(dest, MPSArcDir), MPSDir)
  
  print "Setting mps.vmoptions"
#TODO 
  print "NOT IMPLEMENTED"
  
  print "Cloning mbeddr..."
  cloneMbeddr(dest);
  
  print "Setting up mbeddr..."
#TODO 
  print "NOT IMPLEMENTED"
  
  print "Building mbeddr..."
#TODO 
  print "NOT IMPLEMENTED"
  
  
  print "Welcome to mbeddr. C the difference C the future.";
  
main();