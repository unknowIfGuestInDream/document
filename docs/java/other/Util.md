## 带时间的缓存工具类-CacheUtils

```java
/**
 * 缓存
 *
 * @author: TangLiang
 * @date: 2020/6/4 9:08
 * @since: 1.0
 */
public class CacheUtils {
    /*
     * 预缓存信息
     */
    private static final Map<String, Object> CACHE_MAP = new ConcurrentHashMap<String, Object>();

    /*
    缓存不失效
     */
    public static final long CACHE_HOLD_FOREVER = -1L;

    /**
     * 存放一个缓存对象，默认缓存不失效
     *
     * @param cacheName
     * @param obj
     */
    public static void put(String cacheName, Object obj) {
        put(cacheName, obj, CACHE_HOLD_FOREVER);
    }

    /**
     * 存放一个缓存对象，保存时间为holdTime
     *
     * @param cacheName
     * @param obj
     * @param holdTime
     */
    public static void put(String cacheName, Object obj, long holdTime) {
        CACHE_MAP.put(cacheName, obj);
        if (holdTime > 0L) {
            CACHE_MAP.put(cacheName + "_HoldTime", System.currentTimeMillis() + holdTime);//缓存失效时间
        }
    }

    /**
     * 取出一个缓存对象
     *
     * @param cacheName
     * @return
     */
    public static Object get(String cacheName) {
        if (checkCacheName(cacheName)) {
            return CACHE_MAP.get(cacheName);
        }
        return null;
    }

    /**
     * 删除所有缓存
     */
    public static void removeAll() {
        CACHE_MAP.clear();
    }

    /**
     * 删除某个缓存
     *
     * @param cacheName
     */
    public static void remove(String cacheName) {
        CACHE_MAP.remove(cacheName);
        CACHE_MAP.remove(cacheName + "_HoldTime");
    }

    /**
     * 检查缓存对象是否存在，
     * 若不存在，则返回false
     * 若存在，检查其是否已过有效期，如果已经过了则删除该缓存并返回false
     *
     * @param cacheName
     * @return
     */
    public static boolean checkCacheName(String cacheName) {
        if (!CACHE_MAP.containsKey(cacheName)) {
            return false;
        }
        if (!CACHE_MAP.containsKey(cacheName + "_HoldTime")) {
            return true;
        }
        Long cacheHoldTime = (Long) CACHE_MAP.get(cacheName + "_HoldTime");
        if (cacheHoldTime < System.currentTimeMillis()) {
            remove(cacheName);
            return false;
        }
        return true;
    }
}
```

!> 缺陷是过时缓存不会删除，得在下一次命中时才会删除过期缓存，可以新增定时任务来处理

## 通过延迟队列实现的缓存工具类-Cache

解决上面的过时缓存不会删除的缺陷, 缺点是随着cache的增多，线程随之增加，但是可以改为静态容器统一存储来解决问题

```java
/**
 * 具有过期时间的缓存
 * 向缓存添加内容时，给每一个key设定过期时间，系统自动将超过过期时间的key清除。
 * <p>
 * 当向缓存中添加key-value对时，如果这个key在缓存中存在并且还没有过期，需要用这个key对应的新过期时间
 * 为了能够让DelayQueue将其已保存的key删除，需要重写实现Delayed接口添加到DelayQueue的DelayedItem的hashCode函数和equals函数
 * 当缓存关闭，监控程序也应关闭，因而监控线程应当用守护线程
 *
 * @author: TangLiang
 * @date: 2021/6/29 14:35
 * @since: 1.0
 */
public class Cache<K, V> {

    //存储缓存
    public ConcurrentHashMap<K, V> map = new ConcurrentHashMap<K, V>();
    //延迟队列
    public DelayQueue<DelayedItem<K>> queue = new DelayQueue<DelayedItem<K>>();
    //缓存30秒
    public static final long CACHE_HOLD_30SECOND = 30 * 1000 * 1000 * 1000L;
    //缓存1分钟
    public static final long CACHE_HOLD_1MINUTE = 60 * 1000 * 1000 * 1000L;
    //缓存1天
    public static final long CACHE_HOLD_1DAY = 24 * 60 * 60 * 1000 * 1000 * 1000L;

    /**
     * 缓存值
     */
    public void put(K k, V v, long liveTime) {
        V v2 = map.put(k, v);
        DelayedItem<K> tmpItem = new DelayedItem<K>(k, liveTime);
        if (v2 != null) {
            queue.remove(tmpItem);
        }
        queue.put(tmpItem);
    }

    /**
     * 缓存值 默认缓存一天
     */
    public void put(K k, V v) {
        put(k, v, CACHE_HOLD_1DAY);
    }

    //清空缓存
    public void clear() {
        queue.clear();
        map.clear();
    }

    /**
     * 取出一个缓存对象
     *
     * @param cacheName 缓存名称
     */
    public Object get(String cacheName) {
        return map.get(cacheName);
    }

    public Cache() {
        Thread t = new Thread() {
            @Override
            public void run() {
                dameonCheckOverdueKey();
            }
        };
        t.setDaemon(true);
        t.start();
    }

    public void dameonCheckOverdueKey() {
        while (true) {
            DelayedItem<K> delayedItem = queue.poll();
            if (delayedItem != null) {
                map.remove(delayedItem.getT());
            }
            try {
                Thread.sleep(300);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

}
```

```java
/**
 * 延迟队列对象
 *
 * @author: TangLiang
 * @date: 2021/6/30 9:12
 * @since: 1.0
 */
public class DelayedItem<T> implements Delayed {
    private T t;
    private long liveTime;
    private long removeTime;

    public DelayedItem(T t, long liveTime) {
        this.setT(t);
        this.liveTime = liveTime;
        this.removeTime = TimeUnit.NANOSECONDS.convert(liveTime, TimeUnit.NANOSECONDS) + System.nanoTime();
    }

    @Override
    public int compareTo(Delayed o) {
        if (o == null) return 1;
        if (o == this) return 0;
        if (o instanceof DelayedItem) {
            DelayedItem<T> tmpDelayedItem = (DelayedItem<T>) o;
            if (liveTime > tmpDelayedItem.liveTime) {
                return 1;
            } else if (liveTime == tmpDelayedItem.liveTime) {
                return 0;
            } else {
                return -1;
            }
        }
        long diff = getDelay(TimeUnit.NANOSECONDS) - o.getDelay(TimeUnit.NANOSECONDS);
        return diff > 0 ? 1 : diff == 0 ? 0 : -1;
    }

    @Override
    public long getDelay(TimeUnit unit) {
        return unit.convert(removeTime - System.nanoTime(), unit);
    }

    public T getT() {
        return t;
    }

    public void setT(T t) {
        this.t = t;
    }

    @Override
    public int hashCode() {
        return t.hashCode();
    }

    @Override
    public boolean equals(Object object) {
        if (object instanceof DelayedItem) {
            return object.hashCode() == hashCode() ? true : false;
        }
        return false;
    }
}
```

## 精确的浮点数运算-ArithUtil

double不准确 转换成BigDecimal进行计算

```java
/**
 * 精确的浮点数运算
 * 
 * @author TangLiang
 */
public class ArithUtil
{

    /** 默认除法运算精度 */
    private static final int DEF_DIV_SCALE = 10;

    /** 这个类不能实例化 */
    private Arith()
    {
    }

    /**
     * 提供精确的加法运算。
     * @param v1 被加数
     * @param v2 加数
     * @return 两个参数的和
     */
    public static double add(double v1, double v2)
    {
        BigDecimal b1 = new BigDecimal(Double.toString(v1));
        BigDecimal b2 = new BigDecimal(Double.toString(v2));
        return b1.add(b2).doubleValue();
    }

    /**
     * 提供精确的减法运算。
     * @param v1 被减数
     * @param v2 减数
     * @return 两个参数的差
     */
    public static double sub(double v1, double v2)
    {
        BigDecimal b1 = new BigDecimal(Double.toString(v1));
        BigDecimal b2 = new BigDecimal(Double.toString(v2));
        return b1.subtract(b2).doubleValue();
    }

    /**
     * 提供精确的乘法运算。
     * @param v1 被乘数
     * @param v2 乘数
     * @return 两个参数的积
     */
    public static double mul(double v1, double v2)
    {
        BigDecimal b1 = new BigDecimal(Double.toString(v1));
        BigDecimal b2 = new BigDecimal(Double.toString(v2));
        return b1.multiply(b2).doubleValue();
    }

    /**
     * 提供（相对）精确的除法运算，当发生除不尽的情况时，精确到
     * 小数点以后10位，以后的数字四舍五入。
     * @param v1 被除数
     * @param v2 除数
     * @return 两个参数的商
     */
    public static double div(double v1, double v2)
    {
        return div(v1, v2, DEF_DIV_SCALE);
    }

    /**
     * 提供（相对）精确的除法运算。当发生除不尽的情况时，由scale参数指
     * 定精度，以后的数字四舍五入。
     * @param v1 被除数
     * @param v2 除数
     * @param scale 表示表示需要精确到小数点以后几位。
     * @return 两个参数的商
     */
    public static double div(double v1, double v2, int scale)
    {
        if (scale < 0)
        {
            throw new IllegalArgumentException(
                    "The scale must be a positive integer or zero");
        }
        BigDecimal b1 = new BigDecimal(Double.toString(v1));
        BigDecimal b2 = new BigDecimal(Double.toString(v2));
        if (b1.compareTo(BigDecimal.ZERO) == 0)
        {
            return BigDecimal.ZERO.doubleValue();
        }
        return b1.divide(b2, scale, RoundingMode.HALF_UP).doubleValue();
    }

    /**
     * 提供精确的小数位四舍五入处理。
     * @param v 需要四舍五入的数字
     * @param scale 小数点后保留几位
     * @return 四舍五入后的结果
     */
    public static double round(double v, int scale)
    {
        if (scale < 0)
        {
            throw new IllegalArgumentException(
                    "The scale must be a positive integer or zero");
        }
        BigDecimal b = new BigDecimal(Double.toString(v));
        BigDecimal one = new BigDecimal("1");
        return b.divide(one, scale, RoundingMode.HALF_UP).doubleValue();
    }
}
```

## 身份证/手机号/邮箱校验-CodeUtils

!> 身份证/手机号/邮箱等信息校验并非一直不变的，根据官方政策自行修改

```java
/**
 * @author: TangLiang
 * @date: 2020/9/8 15:23
 * @since: 1.0
 */
public class CodeUtils {

    /**
     * @param IDStr
     * @return String
     * @throws ParseException
     * @description:验证主方法，里面会调用所有方法来验证 2016年5月22日
     */
    public static String IDCardValidate(String IDStr) throws ParseException {
        String tipInfo = "身份证号码正确";// 记录错误信息
        String Ai = "";
        // 判断号码的长度 15位或18位
        if (IDStr.length() != 15 && IDStr.length() != 18) {
            tipInfo = "身份证号码长度应该为15位或18位。";
            return tipInfo;
        }

        // 18位身份证前17位位数字，如果是15位的身份证则所有号码都为数字
        if (IDStr.length() == 18) {
            Ai = IDStr.substring(0, 17);
        } else if (IDStr.length() == 15) {
            Ai = IDStr.substring(0, 6) + "19" + IDStr.substring(6, 15);
        }
        if (isNumeric(Ai) == false) {
            tipInfo = "身份证15位号码都应为数字 ; 18位号码除最后一位外，都应为数字。";
            return tipInfo;
        }

        // 判断出生年月是否有效
        String strYear = Ai.substring(6, 10);// 年份
        String strMonth = Ai.substring(10, 12);// 月份
        String strDay = Ai.substring(12, 14);// 日期
        if (isDate(strYear + "-" + strMonth + "-" + strDay) == false) {
            tipInfo = "身份证出生日期无效。";
            return tipInfo;
        }
        GregorianCalendar gc = new GregorianCalendar();
        SimpleDateFormat s = new SimpleDateFormat("yyyy-MM-dd");
        try {
            if ((gc.get(Calendar.YEAR) - Integer.parseInt(strYear)) > 150
                    || (gc.getTime().getTime() - s.parse(
                    strYear + "-" + strMonth + "-" + strDay).getTime()) < 0) {
                tipInfo = "身份证生日不在有效范围。";
                return tipInfo;
            }
        } catch (NumberFormatException e) {
            e.printStackTrace();
        }
        if (Integer.parseInt(strMonth) > 12 || Integer.parseInt(strMonth) == 0) {
            tipInfo = "身份证月份无效";
            return tipInfo;
        }
        if (Integer.parseInt(strDay) > 31 || Integer.parseInt(strDay) == 0) {
            tipInfo = "身份证日期无效";
            return tipInfo;
        }

        // 判断地区码是否有效
        Hashtable areacode = GetAreaCode();
        //如果身份证前两位的地区码不在Hashtable，则地区码有误
        if (areacode.get(Ai.substring(0, 2)) == null) {
            tipInfo = "身份证地区编码错误。";
            return tipInfo;
        }

        if (isVarifyCode(Ai, IDStr) == false) {
            tipInfo = "身份证校验码无效，不是合法的身份证号码";
            return tipInfo;
        }

        return tipInfo;
    }


     /*
      判断第18位校验码是否正确
      第18位校验码的计算方式：
        　　1. 对前17位数字本体码加权求和
        　　公式为：S = Sum(Ai * Wi), i = 0, ... , 16
        　　其中Ai表示第i个位置上的身份证号码数字值，Wi表示第i位置上的加权因子，其各位对应的值依次为： 7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
        　　2. 用11对计算结果取模
        　　Y = mod(S, 11)
        　　3. 根据模的值得到对应的校验码
        　　对应关系为：
        　　 Y值：     0  1  2  3  4  5  6  7  8  9  10
        　　校验码： 1  0  X  9  8  7  6  5  4  3   2
     */

    /**
     * @param Ai
     * @param IDStr
     * @return
     * @description: 用于计算验证身份证号码最后一位的正确性
     * 2016年5月22日
     */
    private static boolean isVarifyCode(String Ai, String IDStr) {
        String[] VarifyCode = {"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"};
        String[] Wi = {"7", "9", "10", "5", "8", "4", "2", "1", "6", "3", "7", "9", "10", "5", "8", "4", "2"};
        int sum = 0;
        for (int i = 0; i < 17; i++) {
            sum = sum + Integer.parseInt(String.valueOf(Ai.charAt(i))) * Integer.parseInt(Wi[i]);
        }
        int modValue = sum % 11;
        String strVerifyCode = VarifyCode[modValue];
        Ai = Ai + strVerifyCode;
        if (IDStr.length() == 18) {
            return Ai.equals(IDStr);
        }
        return true;
    }


    /**
     * @return Hashtable 对象
     * 将所有地址编码保存在一个Hashtable中
     */
    @SuppressWarnings("unchecked")
    private static Hashtable GetAreaCode() {
        Hashtable hashtable = new Hashtable();
        hashtable.put("11", "北京");
        hashtable.put("12", "天津");
        hashtable.put("13", "河北");
        hashtable.put("14", "山西");
        hashtable.put("15", "内蒙古");
        hashtable.put("21", "辽宁");
        hashtable.put("22", "吉林");
        hashtable.put("23", "黑龙江");
        hashtable.put("31", "上海");
        hashtable.put("32", "江苏");
        hashtable.put("33", "浙江");
        hashtable.put("34", "安徽");
        hashtable.put("35", "福建");
        hashtable.put("36", "江西");
        hashtable.put("37", "山东");
        hashtable.put("41", "河南");
        hashtable.put("42", "湖北");
        hashtable.put("43", "湖南");
        hashtable.put("44", "广东");
        hashtable.put("45", "广西");
        hashtable.put("46", "海南");
        hashtable.put("50", "重庆");
        hashtable.put("51", "四川");
        hashtable.put("52", "贵州");
        hashtable.put("53", "云南");
        hashtable.put("54", "西藏");
        hashtable.put("61", "陕西");
        hashtable.put("62", "甘肃");
        hashtable.put("63", "青海");
        hashtable.put("64", "宁夏");
        hashtable.put("65", "新疆");
        hashtable.put("71", "台湾");
        hashtable.put("81", "香港");
        hashtable.put("82", "澳门");
        hashtable.put("91", "国外");
        return hashtable;
    }

    /**
     * @param strnum 数字
     * @return 判断字符串是否为数字, 0-9重复0次或者多次
     */
    private static boolean isNumeric(String strnum) {
        Pattern pattern = Pattern.compile("[0-9]*");
        Matcher isNum = pattern.matcher(strnum);
        return isNum.matches();
    }

    /**
     * @param strDate 日期
     * @return 功能：判断字符串出生日期是否符合正则表达式：包括年月日，闰年、平年和每月31天、30天和闰月的28天或者29天
     */
    public static boolean isDate(String strDate) {

        Pattern pattern = Pattern
                .compile("^((\\d{2}(([02468][048])|([13579][26]))[\\-\\/\\s]?((((0?[13578])|(1[02]))[\\-\\/\\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\\-\\/\\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\\-\\/\\s]?((0?[1-9])|([1-2][0-9])))))|(\\d{2}(([02468][1235679])|([13579][01345789]))[\\-\\/\\s]?((((0?[13578])|(1[02]))[\\-\\/\\s]?((0?[1-9])|([1-2][0-9])|(3[01])))|(((0?[469])|(11))[\\-\\/\\s]?((0?[1-9])|([1-2][0-9])|(30)))|(0?2[\\-\\/\\s]?((0?[1-9])|(1[0-9])|(2[0-8]))))))?$");
        Matcher m = pattern.matcher(strDate);
        return m.matches();
    }

    /**
     * 验证手机号是否合法
     *
     * @return boolean
     */
    public static boolean isMobileNumber(String number) {
        if (StringUtils.isEmpty(number)) {
            return false;
        }
        if (11 != number.length()) {
            return false;
        }
        /*
         * 移动号段正则表达式
         */
        String pat1 = "^((13[4-9])|(147)|(15[0-2,7-9])|(178)|(18[2-4,7-8]))\\d{8}|(1705)\\d{7}$";
        /*
         * 联通号段正则表达式
         */
        String pat2 = "^((13[0-2])|(145)|(15[5-6])|(176)|(18[5,6]))\\d{8}|(1709)\\d{7}$";
        /*
         * 电信号段正则表达式
         */
        String pat3 = "^((133)|(153)|(177)|(18[0,1,9])|(149))\\d{8}$";
        /*
         * 虚拟运营商正则表达式
         */
        String pat4 = "^((170))\\d{8}|(1718)|(1719)\\d{7}$";

        Pattern pattern1 = Pattern.compile(pat1);
        Matcher match1 = pattern1.matcher(number);
        boolean isMatch1 = match1.matches();
        if (isMatch1) {
            return true;
        }
        Pattern pattern2 = Pattern.compile(pat2);
        Matcher match2 = pattern2.matcher(number);
        boolean isMatch2 = match2.matches();
        if (isMatch2) {
            return true;
        }
        Pattern pattern3 = Pattern.compile(pat3);
        Matcher match3 = pattern3.matcher(number);
        boolean isMatch3 = match3.matches();
        if (isMatch3) {
            return true;
        }
        Pattern pattern4 = Pattern.compile(pat4);
        Matcher match4 = pattern4.matcher(number);
        boolean isMatch4 = match4.matches();
        if (isMatch4) {
            return true;
        }
        return false;
    }

    /**
     * 判断该邮件地址是否合法
     *
     * @param address 邮件地址，可以多个，逗号隔开
     * @return boolean
     */
    public static boolean isEmailAddress(String address) {
        // 是否合法
        boolean flag = false;
        if (StringUtils.isEmpty(address)) {
            return false;
        }
        try {
            String[] addressArr = address.split(",");
            String check = "^([a-z0-9A-Z]+[-|_|\\.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-zA-Z]{2,}$";
            Pattern regex = Pattern.compile(check);
            Matcher matcher = null;
            for (String str : addressArr) {
                matcher = regex.matcher(str);
                flag = matcher.matches();
                if (!flag) {
                    return false;
                }
            }
        } catch (Exception e) {
            flag = false;
        }
        return flag;
    }

    /**
     * 用户身份证号码的打码隐藏加星号加*
     *
     * @return 处理完成的身份证
     */
    public static String idCardMask(String idCardNum) {
        String res = "";
        if (!StringUtils.isEmpty(idCardNum)) {
            StringBuilder stringBuilder = new StringBuilder(idCardNum);
            res = stringBuilder.replace(6, 14, "********").toString();
        }
        return res;
    }

    /**
     * 用户电话号码的打码隐藏加星号加*
     *
     * @return 处理完成的身份证
     */
    public static String phoneMask(String phone) {
        String res = "";
        if (!StringUtils.isEmpty(phone)) {
            StringBuilder stringBuilder = new StringBuilder(phone);
            res = stringBuilder.replace(3, 7, "****").toString();
        }
        return res;
    }

}
```

## 通过LinkedHashMap实现LRU缓存

```java
public class LRUCache<K, V> {
    private static final float hashTableLoadFactor = 0.75f;
    private LinkedHashMap<K, V> map;//用于存放缓存的k-v
    private int cacheSize;// 缓存的k-v的个数

    /**
     * Creates a new LRU cache. 在该方法中，new LinkedHashMap<K,V>(hashTableCapacity,
     * hashTableLoadFactor, true)中，true代表使用访问顺序
     *
     * @param cacheSize
     *            the maximum number of entries that will be kept in this cache.
     */
    public LRUCache(int cacheSize) {
        this.cacheSize = cacheSize;
        int hashTableCapacity = (int) Math
                .ceil(cacheSize / hashTableLoadFactor) + 1;
        map = new LinkedHashMap<K, V>(hashTableCapacity, hashTableLoadFactor,
                true) {// 设置为true，才能够满足LRU缓存功能1：“最近访问的放最前”
            // (an anonymous inner class)
            private static final long serialVersionUID = 1;

            // 重写该方法，才能够实现LUR缓存功能2：“空间不足，删除最不常用的元素”
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > LRUCache.this.cacheSize;
            }
        };
    }

    /**
     * Retrieves an entry from the cache.<br>
     * The retrieved entry becomes the MRU (most recently used) entry.
     *
     * @param key
     *            the key whose associated value is to be returned.
     * @return the value associated to this key, or null if no value with this
     *         key exists in the cache.
     */
    public synchronized V get(K key) {
        return map.get(key);
    }

    /**
     * Adds an entry to this cache. The new entry becomes the MRU (most recently
     * used) entry. If an entry with the specified key already exists in the
     * cache, it is replaced by the new entry. If the cache is full, the LRU
     * (least recently used) entry is removed from the cache.
     *
     * @param key
     *            the key with which the specified value is to be associated.
     * @param value
     *            a value to be associated with the specified key.
     */
    public synchronized void put(K key, V value) {
        map.put(key, value);
    }

    /**
     * Clears the cache.
     */
    public synchronized void clear() {
        map.clear();
    }

    /**
     * Returns the number of used entries in the cache.
     *
     * @return the number of entries currently in the cache.
     */
    public synchronized int usedEntries() {
        return map.size();
    }

    /**
     * Returns a <code>Collection</code> that contains a copy of all cache
     * entries.
     *
     * @return a <code>Collection</code> with a copy of the cache content.
     */
    public synchronized Collection<Map.Entry<K, V>> getAll() {
        return new ArrayList<Map.Entry<K, V>>(map.entrySet());
    }

    // Test routine for the LRUCache class.
    public static void main(String[] args) {
        LRUCache<String, String> c = new LRUCache<String, String>(3);
        c.put("1", "one"); // 1
        c.put("2", "two"); // 2 1
        c.put("3", "three"); // 3 2 1
        c.put("4", "four"); // 4 3 2
        if (c.get("2") == null)
            throw new Error(); // 2 4 3
        c.put("5", "five"); // 5 2 4
        c.put("4", "second four"); // 4 5 2
        // Verify cache content.
        if (c.usedEntries() != 3)
            throw new Error();
        if (!c.get("4").equals("second four"))
            throw new Error();
        if (!c.get("5").equals("five"))
            throw new Error();
        if (!c.get("2").equals("two"))
            throw new Error();
        // List cache content.
        for (Map.Entry<String, String> e : c.getAll())
            System.out.println(e.getKey() + " : " + e.getValue());
    }
}
```

## 首字母大/小写

```java
public class util{
    /**
     * 首字母大写
     *
     * @param string
     * @return
     */
    public static String toUpperCase4Index(String string) {
        char[] methodName = string.toCharArray();
        methodName[0] = toUpperCase(methodName[0]);
        return String.valueOf(methodName);
    }

    /**
     * 字符转成大写
     *
     * @param chars
     * @return
     */
    public static char toUpperCase(char chars) {
        if (97 <= chars && chars <= 122) {
            chars ^= 32;
        }
        return chars;
    }

    /**
     * 首字母小写
     *
     * @param string
     * @return
     */
    public static String toLowerCase4Index(String string) {
        if (Character.isLowerCase(string.charAt(0))) {
            return string;
        }

        char[] chars = string.toCharArray();
        chars[0] += 32;
        return String.valueOf(chars);
    }
}
```

## list转换tree
主要处理List<Map<String, Object>>结构数据，来源为数据库查询结果

```java
public class ListToTreeUtil {
    /**
     * 并发除法阈值，容器大于此值走并发流提高性能
     */
    private static final int FILL_PALL = 500;
    /**
     * 默认是否进行深拷贝，false不进行深拷贝
     */
    private static final boolean DEFAULT_DEEP = false;

    /**
     * list转换为tree结构数据
     *
     * @param list      数据
     * @param isRoot    判断为根节点的函数
     * @param idFun     id函数
     * @param pidFun    上级id函数
     * @param deepClone 是否进行深克隆，默认为否
     */
    public static List<Map<String, Object>> listToTree(List<Map<String, Object>> list, Predicate<Map<String, Object>> isRoot, Function<Map<String, Object>, ?> idFun, Function<Map<String, Object>, ?> pidFun, boolean deepClone) {
        if (Objects.isNull(list) || Objects.isNull(isRoot) || Objects.isNull(idFun) || Objects.isNull(pidFun)) {
            return new ArrayList<>();
        }
        List<Map<String, Object>> cloneList = list;
        if (deepClone) {
            cloneList = (List<Map<String, Object>>) BaseUtils.deepClone(list);
        }
        //方法复杂度为O(n2)数据量超过一百条时走并发流优化性能
        List<Map<String, Object>> children;
        if (list.size() > FILL_PALL) {
            children = Collections.synchronizedList(new ArrayList<>());
            List<Map<String, Object>> finalCloneList = Collections.synchronizedList(cloneList);
            cloneList.parallelStream()
                    .filter(isRoot).forEachOrdered(s -> {
                children.add(s);
                fillChild(s, finalCloneList, idFun, pidFun);
            });
        } else {
            children = new ArrayList<>();
            for (Map<String, Object> child : cloneList) {
                if (isRoot.test(child)) {
                    children.add(child);
                    fillChild(child, cloneList, idFun, pidFun);
                }
            }
        }

        return children;
    }

    /**
     * list转换为tree结构数据
     *
     * @param list      数据
     * @param isRoot    判断为根节点的函数
     * @param idField   id字段
     * @param pidField  上级id字段
     * @param deepClone 是否进行深克隆，默认为否
     */
    public static List<Map<String, Object>> listToTree(List<Map<String, Object>> list, Predicate<Map<String, Object>> isRoot, String idField, String pidField, boolean deepClone) {
        return listToTree(list, isRoot, (m) -> m.get(idField), (n) -> n.get(pidField), deepClone);
    }

    public static List<Map<String, Object>> listToTree(List<Map<String, Object>> list, Predicate<Map<String, Object>> isRoot, String idField, String pidField) {
        return listToTree(list, isRoot, idField, pidField, DEFAULT_DEEP);
    }

    public static List<Map<String, Object>> listToTree(List<Map<String, Object>> list, Predicate<Map<String, Object>> isRoot, Function<Map<String, Object>, ?> idFun, Function<Map<String, Object>, ?> pidFun) {
        return listToTree(list, isRoot, idFun, pidFun, DEFAULT_DEEP);
    }

    /**
     * 递归生成树节点
     *
     * @param child  每个元素
     * @param list   数据集
     * @param idFun  id函数
     * @param pidFun 上级id函数
     */
    private static void fillChild(Map<String, Object> child, List<Map<String, Object>> list, Function<Map<String, Object>, ?> idFun, Function<Map<String, Object>, ?> pidFun) {
        List<Map<String, Object>> children;
        if (list.size() > FILL_PALL) {
            children = Collections.synchronizedList(new ArrayList<>());
            list.parallelStream().filter(s -> idFun.apply(child).equals(pidFun.apply(s))).forEachOrdered(s -> {
                children.add(s);
                fillChild(s, list, idFun, pidFun);
            });
        } else {
            children = new ArrayList<>();
            for (Map<String, Object> childDiv : list) {
                if (idFun.apply(child).equals(pidFun.apply(childDiv))) {
                    children.add(childDiv);
                    fillChild(childDiv, list, idFun, pidFun);
                }
            }
        }

        child.put("children", children);
    }
}
```

测试类
```java
@SpringBootTest
public class ListToTreeTest {
    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void listToTree() throws JsonProcessingException {
        List<Map<String, Object>> list = new ArrayList<>();
        init(list);
        List<Map<String, Object>> children = ListToTreeUtil.listToTree(list, (m) -> "-1".equals(m.get("PID")), "ID", "PID", true);
        List<Map<String, Object>> children1 = ListToTreeUtil.listToTree(list, (m) -> "-1".equals(m.get("PID")), (m) -> m.get("ID"), (n) -> n.get("PID"), true);
        System.out.println(objectMapper.writeValueAsString(list));
        System.out.println(objectMapper.writeValueAsString(children));
        System.out.println(objectMapper.writeValueAsString(children1));
    }

    public void init(List<Map<String, Object>> list) {
        Map<String, Object> map1 = new HashMap<>();
        map1.put("ID", "1");
        map1.put("PID", "-1");
        list.add(map1);
        Map<String, Object> map2 = new HashMap<>();
        map2.put("ID", "2");
        map2.put("PID", "1");
        list.add(map2);
        Map<String, Object> map3 = new HashMap<>();
        map3.put("ID", "3");
        map3.put("PID", "2");
        list.add(map3);
        Map<String, Object> ma4 = new HashMap<>();
        ma4.put("ID", "4");
        ma4.put("PID", "2");
        list.add(ma4);
    }

}
```

## BigDecimal批量计算
由于除法涉及精度，需要传int类型的参数，故无int类型的批量除法，只能单个相除

```java
public class BigDecimalBuilder {
    private BigDecimal bigDecimal;
    /**
     * 默认除法运算精度
     */
    private final int DEF_DIV_SCALE = 2;

    //构造器
    private BigDecimalBuilder(int i) {
        this.bigDecimal = new BigDecimal(i);
    }

    private BigDecimalBuilder(String str) {
        this.bigDecimal = new BigDecimal(str);
    }

    private BigDecimalBuilder(double d) {
        this.bigDecimal = new BigDecimal(d);
    }

    private void set(BigDecimal decimal) {
        this.bigDecimal = decimal;
    }

    public static BigDecimalBuilder builder(int i) {
        return new BigDecimalBuilder(i);
    }

    public static BigDecimalBuilder builder(String str) {
        return new BigDecimalBuilder(str);
    }

    public static BigDecimalBuilder builder(double d) {
        return new BigDecimalBuilder(d);
    }

    public BigDecimalBuilder add(String... strs) {
        for (String str : strs) {
            set(bigDecimal.add(new BigDecimal(str)));
        }
        return this;
    }

    public BigDecimalBuilder add(double... doubles) {
        for (double d : doubles) {
            set(bigDecimal.add(BigDecimal.valueOf(d)));
        }
        return this;
    }

    public BigDecimalBuilder add(int... ints) {
        for (int i : ints) {
            set(bigDecimal.add(BigDecimal.valueOf(i)));
        }
        return this;
    }

    public BigDecimalBuilder sub(String... strs) {
        for (String str : strs) {
            set(bigDecimal.subtract(new BigDecimal(str)));
        }
        return this;
    }

    public BigDecimalBuilder sub(double... doubles) {
        for (double d : doubles) {
            set(bigDecimal.subtract(BigDecimal.valueOf(d)));
        }
        return this;
    }

    public BigDecimalBuilder sub(int... ints) {
        for (int i : ints) {
            set(bigDecimal.subtract(BigDecimal.valueOf(i)));
        }
        return this;
    }

    public BigDecimalBuilder mul(String... strs) {
        for (String str : strs) {
            set(bigDecimal.multiply(new BigDecimal(str)));
        }
        return this;
    }

    public BigDecimalBuilder mul(double... doubles) {
        for (double d : doubles) {
            set(bigDecimal.multiply(BigDecimal.valueOf(d)));
        }
        return this;
    }

    public BigDecimalBuilder mul(int... ints) {
        for (int i : ints) {
            set(bigDecimal.multiply(BigDecimal.valueOf(i)));
        }
        return this;
    }

    /**
     * 提供（相对）精确的除法运算。当发生除不尽的情况时，由scale参数指
     * 定精度(默认2位)，以后的数字四舍五入。
     */
    public BigDecimalBuilder div(String... strs) {
        div(DEF_DIV_SCALE, strs);
        return this;
    }

    public BigDecimalBuilder div(double... doubles) {
        div(DEF_DIV_SCALE, doubles);
        return this;
    }

    public BigDecimalBuilder div(int scale, String... strs) {
        for (String str : strs) {
            set(bigDecimal.divide(new BigDecimal(str), scale, RoundingMode.HALF_UP));
        }
        return this;
    }

    public BigDecimalBuilder div(int scale, double... doubles) {
        for (double d : doubles) {
            set(bigDecimal.divide(BigDecimal.valueOf(d), scale, RoundingMode.HALF_UP));
        }
        return this;
    }

    /**
     * 由于需要传入小数精度，故int的类型入参不支持批量相除
     */
    public BigDecimalBuilder div(int scale, int i) {
        set(bigDecimal.divide(BigDecimal.valueOf(i), scale, RoundingMode.HALF_UP));
        return this;
    }

    /**
     * 提供精确的小数位四舍五入处理。
     *
     * @param scale 小数点后保留几位, 默认2位
     * @return 四舍五入后的结果
     */
    public BigDecimalBuilder round(int scale) {
        if (scale < 0) {
            throw new IllegalArgumentException(
                    "The scale must be a positive integer or zero");
        }
        set(bigDecimal.divide(BigDecimal.ONE, scale, RoundingMode.HALF_UP));
        return this;
    }

    public BigDecimalBuilder round() {
        round(DEF_DIV_SCALE);
        return this;
    }

    public BigDecimal build() {
        return bigDecimal;
    }
}
```

测试类
```java
@SpringBootTest
public class BigDecimalBuilderTest {

    @Test
    public void addTest() {
        BigDecimal bigDecimal = BigDecimalBuilder.builder(1).add("2", "3").add(3.2, 2.1).build();
        System.out.println(bigDecimal);
    }

    @Test
    public void subTest() {
        BigDecimal bigDecimal = BigDecimalBuilder.builder(2).sub(1).sub(1.1).sub("3").build();
        System.out.println(bigDecimal);
    }

    @Test
    public void mulTest() {
        BigDecimal bigDecimal = BigDecimalBuilder.builder(2).mul(2, 3, 4).mul("2", "2").build();
        System.out.println(bigDecimal);
    }

    @Test
    public void divTest() {
        BigDecimal bigDecimal1 = BigDecimalBuilder.builder(64).div("2", "2").build();
        System.out.println(bigDecimal1);
        BigDecimal bigDecimal2 = BigDecimalBuilder.builder(64).div(4, "2", "2").build();
        System.out.println(bigDecimal2);
    }

    @Test
    public void roundTest() {
        BigDecimal bigDecimal1 = BigDecimalBuilder.builder(64).div(4, "2", "2").round().build();
        System.out.println(bigDecimal1);
    }

    @Test
    public void airthTest() {
        BigDecimal bigDecimal1 = BigDecimalBuilder.builder(1).add(2, 3).sub(2, 0).div("3").build();
        System.out.println(bigDecimal1);
    }
}
```