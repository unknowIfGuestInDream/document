## TreeMap
1. TreeMap存储K-V键值对，通过红黑树（R-B tree）实现；
2. TreeMap继承了NavigableMap接口，NavigableMap接口继承了SortedMap接口，可支持一系列的导航定位以及导航操作的方法，当然只是提供了接口，需要TreeMap自己去实现；
3. TreeMap实现了Cloneable接口，可被克隆，实现了Serializable接口，可序列化；
4. TreeMap因为是通过红黑树实现，红黑树结构天然支持排序，默认情况下通过Key值的自然顺序进行排序；

### 重写排序

```java

public class T_TreeMap {
 
	public static void main(String[] args) {
//根据value排序
		HashMap<Integer,MyRectangle> hh = new HashMap<Integer,MyRectangle>();
		hh.put(2, new MyRectangle(3,6));
		hh.put(4, new MyRectangle(4,4));
		hh.put(1, new MyRectangle(3,7));
		hh.put(5, new MyRectangle(5,4));
		hh.put(3, new MyRectangle(6,2));
				
		List<Entry<Integer,MyRectangle>> list = new ArrayList<Entry<Integer,MyRectangle>>(hh.entrySet());	
		Collections.sort(list,new Comparator<Map.Entry<Integer,MyRectangle>>() {           			     
			public int compare(Entry<Integer,MyRectangle> o1, Entry<Integer,MyRectangle> o2) {             
				return o1.getValue().compareTo(o2.getValue());        
				}        
		});
		for (Entry<Integer,MyRectangle> e: list) {
 
			System.out.println(e.getKey()+":"+e.getValue().Getarea()+" "+e.getValue().Getzc());
 
		}
		Iterator<Entry<Integer, MyRectangle>> rr = hh.entrySet().iterator();
		while(rr.hasNext()) {
			MyRectangle r1 = rr.next().getValue();		
			System.out.println(" " +r1.Getarea());
		}


//根据key排序
                TreeMap<Integer,Integer> map1 = new TreeMap<Integer,Integer>();  //默认的TreeMap升序排列
                TreeMap<Integer,Integer> map2= new TreeMap<Integer,Integer>(new Comparator<Integer>(){
                     /* 
                     * int compare(Object o1, Object o2) 返回一个基本类型的整型， 
                     * 返回负数表示：o1 小于o2， 
                     * 返回0 表示：o1和o2相等， 
                     * 返回正数表示：o1大于o2。 
                     */  
                    public int compare(Integer a,Integer b){
                        return b-a;            
                    }
                    });
                map2.put(1,2);
                map2.put(2,4);
                map2.put(7, 1);
                map2.put(5,2);
                System.out.println("Map2="+map2);  
                
                map1.put(1,2);
                map1.put(2,4);
                map1.put(7, 1);
                map1.put(5,2);
                System.out.println("map1="+map1);
	}
}
```

TreeMap底层是根据红黑树的数据结构构建的，默认是根据key的自然排序来组织（比如integer的大小，String的字典排序）。所以，TreeMap只能根据key来排序，是不能根据value来排序的

如果需要根据value排序的话  
通过Map.Entry里的entrySet方法把所有的Key值和Values值取出来，放在了一个ArrayList集合里，再运用Collections类的方法进行排序