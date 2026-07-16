# Hearth & Harvest is discovered through fabric.mod.json. Keep that public
# entrypoint stable while obfuscating the implementation behind it.
-keep public class com.mirinsworkshop.hearthandharvest.HearthAndHarvest {
    public <init>();
    public void onInitialize();
}

# This release step intentionally focuses on name obfuscation. Disabling code
# removal and optimization avoids changing registry initialization semantics.
-dontshrink
-dontoptimize

-useuniqueclassmembernames
-adaptresourcefilecontents fabric.mod.json
-keepdirectories

-keepattributes Exceptions,InnerClasses,EnclosingMethod,Signature,*Annotation*,Record,SourceFile,LineNumberTable
-renamesourcefileattribute HearthAndHarvest

# Fabric and Minecraft expose optional runtime types that are not all present
# on every dedicated-server class path. They are supplied by the game at run time.
-dontnote
-dontwarn

-printmapping build/proguard/mapping.txt
-printseeds build/proguard/seeds.txt
-printusage build/proguard/usage.txt
