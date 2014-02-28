import sys, os, subprocess, urllib2, platform, tarfile
from os.path import expanduser
import zipfile
import os.path

EAPNum = "27"  
MPSSourceUrl = """http://download-ln.jetbrains.com/mps/31/"""
MPSWin = """MPS-3.1-EAP1-"""+EAPNum+""".exe"""
MPSMac = """MPS-3.1-EAP1-"""+EAPNum+"""-macos.dmg"""
MPSLin = """MPS-3.1-EAP1-"""+EAPNum+""".tar.gz"""
MPSZip = """MPS-3.1-EAP1-"""+EAPNum+""".zip"""

MPSArcDir = """MPS 3.1 EAP"""

MbeddrRepo = """https://github.com/mbeddr/mbeddr.core.git"""

TheBranch = "fortissStable"

Debug = False

InstallJavaMessage= """Please, install a Java (R, TM) from Oracle. 

http://www.oracle.com/technetwork/java/javase/downloads/index.html

On Ubuntu this might work:
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
"""

InstallAntMessage= """Please, install Apache Ant(TM).\n 

http://ant.apache.org/bindownload.cgi

On Ubuntu this might work:
sudo apt-get install ant
"""

InstallGitMessage= """Please, install Git.\n 

http://git-scm.com/downloads

On Ubuntu this might work:
sudo apt-get install git
"""

MPS_VMOPTIONS="""-client
-Xss1024k
-ea
-Xmx2100m
-XX:MaxPermSize=2256m
-XX:NewSize=512m
-XX:+HeapDumpOnOutOfMemoryError
-Dfile.encoding=UTF-8
-Dapple.awt.graphics.UseQuartz=true
-Didea.paths.selector=MPS30
-Didea.config.path=IdeaConfig
-Didea.system.path=IdeaSystem"""
#-Didea.plugins.path=IdeaPlugins"""

LIBRARY_MANAGER = """<?xml version="1.0" encoding="UTF-8"?>
<application>
  <component name="LibraryManager">
    <option name="libraries">
      <map>
        <entry key="mbeddr.core">
          <value>
            <Library>
              <option name="name" value="mbeddr.core" />
              <option name="path" value="${mbeddr.github.core.home}/code" />
            </Library>
          </value>
        </entry>
      </map>
    </option>
  </component>
</application>"""

PATH_MACROS = """<?xml version="1.0" encoding="UTF-8"?>
<application>
  <component name="PathMacrosImpl">
    <macro name="mbeddr.github.core.home" value="MbeddrDir" />
  </component>
</application>
"""

BUILD_PROPERTIES = """# MPS installation
mps.home=MPSDir
# Folder where MPS stores it's cache
mps.platform.caches=MPSCaches
# Points to the root folder of the mbeddr.core repository
mbeddr.github.core.home=MbeddrDir
"""


def checkJavaVersion(java):
  vals = java.split() 
  a = [s for s in vals if "1.6" in s]
  b = [s for s in vals if "1.7" in s]
  c = [s for s in vals if "HotSpot" in s]
  if len(c) > 0:
    if len(a) + len(b) > 0:
      return True;
  return "Java version is not recognized\n"+InstallJavaMessage;
  
  
def checkJava():  
  try:
    java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
    return checkJavaVersion(java)
  except OSError:
    return InstallJavaMessage;

def checkGitVersion(git):
  if "git version" in git:
    return True;
  else:
    return "Unrecognized git version\n"    
   
def checkGit():  
  try:
    git = subprocess.check_output(["git", "--version"], stderr=subprocess.STDOUT)
    return checkGitVersion(git)
  except OSError:
    return InstallGitMessage;
    
    
def checkAntVersion(ant):
  if "Apache Ant" in ant:
    return True;
  else:
    return "Unrecognized ant version\n"
    
def checkAnt():
  try:
    ant = subprocess.check_output(["ant", "-version"], stderr=subprocess.STDOUT)
    return checkAntVersion(ant)
  except OSError:
    return "No ant installed, please install Apache Ant(TM)\n"

  
  
  
def prepareDestDir():
  home = os.path.join(expanduser("~"), "mbeddr")
  print("Where would you like to install it["+home+"]: ")
  try:
    destdir = str(raw_input()).strip()
  except EOFError:
    destdir = None
  
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
  
def MPSFilename():
  url="";
  s = getOs();
  if "Lin" in s:
    url+=MPSLin
  if "Mac" in s:
    url+=MPSMac
  if "Win" in s:
    url+=MPSWin
  return url;

def downloadMPS(dest):
  fName = MPSFilename();
  url = MPSSourceUrl + fName; 
  fName = os.path.join(dest, fName);  
  if os.path.exists(fName):
    return fName;
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
    
def untgz(arc, dest):
  tfile = tarfile.open(arc, 'r:gz');
  tfile.extractall(dest);
  
def unarchive(a, dest):
  if "zip" in a:
    unzip(a, dest);
  else:
    untgz(a, dest);


def cloneMbeddr(dest, MbeddrDir):
  
  if not os.path.exists(MbeddrDir):
    os.makedirs(MbeddrDir);
  else:
    if Debug == True:
      return;
  os.system("git clone " + MbeddrRepo+ " " + MbeddrDir);
  print "Checking out " + TheBranch + " branch..."
  os.system("git --git-dir="+ os.path.join(MbeddrDir, ".git") + " checkout " + TheBranch);
  
  
def configureMpsVmopts(MPSDir, MbeddrDir):
    f = open(os.path.join(MPSDir, "bin", "mps.vmoptions"), 'w');
    opts = MPS_VMOPTIONS;
    ConfigPath = os.path.join(MPSDir, "IdeaConfig");
    if not os.path.exists(ConfigPath):
      os.makedirs(ConfigPath);
    opts = opts.replace("IdeaConfig", ConfigPath);
    
    SysPath = os.path.join(MPSDir, "IdeaSystem");
    
    if not os.path.exists(SysPath):
      os.makedirs(SysPath);
    opts = opts.replace("IdeaSystem", SysPath);
    
    f.write(opts);
    f.close();
    
    OptionsPath = os.path.join(ConfigPath, "options");
    if not os.path.exists(OptionsPath):
      os.makedirs(OptionsPath);
    
    f = open(os.path.join(OptionsPath, "libraryManager.xml"), 'w');
    f.write(LIBRARY_MANAGER);
    f. close();
    
    f = open(os.path.join(OptionsPath, "path.macros.xml"), 'w');
    f.write(PATH_MACROS.replace("MbeddrDir", MbeddrDir));
    f. close();
  
def configureMbeddr(MPSDir, MbeddrDir):
  BuildPropsPath = os.path.join(MbeddrDir, "code", "languages", "build.properties");
  f = open(BuildPropsPath, 'w');
  f.write(BUILD_PROPERTIES.replace("MPSDir", MPSDir).replace("MPSCaches", os.path.join(MPSDir, "CachesMbeddr")).replace(
 "MbeddrDir", MbeddrDir));
  f.close();

def buildMbeddr(MbeddrDir):
  BuildPath = os.path.join(MbeddrDir, "code", "languages");
  os.chdir(BuildPath);
  os.system(os.path.join(BuildPath, "buildLanguages.sh"));

def main():
  print("Welcome!")
  print("You are about to install the last stable version of mbeddr.")

  print "Detecting Git"  
  j = checkGit()
  if j != True:
    print j;
    return 1; 
  
  print "Detecting Java"  
  j = checkJava()
  if j != True:
    print j;
    return 1;  
  
  print "Detecting Ant"
  j = checkAnt()
  if j != True:
    print j;
    return 1;  
  
  print "Preparing destination directory";  
  dest = prepareDestDir();
  if dest == False:
    print "Problem creating destination directory";
    return 1;
  
  MPSDir = os.path.join(dest, "MPS31");
  MbeddrDir = os.path.join(dest, "mbeddr.github");
  
  if os.path.exists(MPSDir) == False or Debug == False:
    print "Downloading MPS..."
    archive = downloadMPS(dest);      
    print "Extracting..."
    unarchive(archive, dest);  
    print "Deleting archive"
    if Debug == False:
      os.remove(archive);    
    print "Renaming MPS folder"    
    os.rename(os.path.join(dest, MPSArcDir), MPSDir)
  
  if os.path.exists(MPSDir) == False or Debug == False:
    print "Cloning mbeddr..."
    cloneMbeddr(dest, MbeddrDir);
  
  print "Setting mps.vmoptions"
  configureMpsVmopts(MPSDir, MbeddrDir);
  
  print "Setting up mbeddr..."
  configureMbeddr(MPSDir, MbeddrDir);

  
  print "Building mbeddr..."
  buildMbeddr(MbeddrDir);
  #Second time, because first time fails shortly after the start,
  buildMbeddr(MbeddrDir);
  
  
  print "Welcome to mbeddr. C the difference C the future.";
  
main();