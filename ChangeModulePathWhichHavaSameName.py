#这一个模块是用来改变module的路径的，比如yolov5和yolov7都用到models模块但是如果一个先加载了，就没办法改变了。用del卸载模块，sys.path.append（添加路径）
#sys.path.remove（删除路径）都不足以解决这个问题。实际上python 用 sys.modules记录所有加载的module的信息，上面几部并不能真正修改这里的信息，需要修改这里的信息，这是一个dict，其中不仅有module还有其子模块比如models和models.common等
#但是第一次sys.path.append的时候加载了很多的模块和子模块，这样就需要一个个删除很麻烦，这里用Trie方法进行关键字模糊删除，可以删除带有关键字的模块。
from collections import defaultdict
class Trie(defaultdict):
    def __init__(self, value=None):
        super().__init__(lambda: Trie(value))  # Trie is essentially hash-table within hash-table
        self.__value = value

    def __getitem__(self, key):
        node = self
        if len(key) > 1:  # allows you to access the trie like this trie["abc"] instead of trie["a"]["b"]["c"]
            for char in key:
                node = node[char]
            return node
        else:  # actual getitem routine
            return defaultdict.__getitem__(self, key)

    def __setitem__(self, key, value):
        node = self
        if len(key) > 1:  # allows you to access the trie like this trie["abc"] instead of trie["a"]["b"]["c"]
            for char in key[:-1]:
                node = node[char]
            node[key[-1]] = value
        else:  # actual setitem routine
            if type(value) is int:
                value = Trie(int(value))
            defaultdict.__setitem__(self, key, value)

    def __str__(self):
        return str(self.__value)
def delSysModules(ModulesList):
    import sys,os 
    
    for m in ModulesList:
        t = Trie()
        t[m.__name__]=1
        for k in sys.modules.keys():
            a=t[k]
            if str(a) == str(1):
                print(k)
                del sys.modules[k]
def ChageModulePath(modulesList,oldpath,newpath):
    import sys,os 
    delSysModules(modulesList)
    sys.path.remove(os.path.dirname(oldpath+'/'))
    sys.path.append(os.path.dirname(newpath+'/'))
