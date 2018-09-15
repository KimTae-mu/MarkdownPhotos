## Two Sum ##

### Question ###

	Given an array of integers, return **indices** of the two numbers such that they add up to a specific target.

You may assume that each input would have **exactly** one solution, and you may not use the *same* element twice.



### Example ###

```java
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1]. 
```

### Solution ###

1. 简单实现:使用target将数组第一个元素减去,遍历之后的元素,若存在相等的结果,返回两数index,否则,减去第二个元素,以此类推.

   ```java
   private int[] towSum(int[] nums, int target) {
           for (int i = 0; i < nums.length; i++) {
               int temp = target - nums[i];
               for (int j = i; j < nums.length; j++) {
                   if (temp == nums[j]) {
                       return new int[]{i, j};
                   }
               }
           }
           return null;
       }
   ```

   按此思路实现后时间复杂度略高.

2. 使用Set和HashMap实现:第一个循环,将数组所有的数字放入HashSet中,创建Map对象<num,index[]>,第二个循环直接遍历nums,在set和map中查找结果.

   ```java
   private int[] towSum_SetAndHashMap(int[] nums, int target) {
           Set<Integer> numSet = new HashSet<>();
           Map<Integer, int[]> indexMap = new HashMap<>();
           for (int i = 0; i < nums.length; i++) {
               if (indexMap.keySet().contains(nums[i])) {
                   int[] index = new int[2];
                   index[0] = indexMap.get(nums[i])[0];
                   index[1] = i;
                   indexMap.put(nums[i], index);
               } else {
                   int[] index = new int[1];
                   index[0] = i;
                   indexMap.put(nums[i], index);
               }
               numSet.add(nums[i]);
           }
   
           for (int num : nums) {
               if (numSet.contains(target - num)) {
                   if (indexMap.get(target - num).length == 1) {
                       if (target - num != num) {
                           return new int[]{indexMap.get(num)[0], indexMap.get(target - num)[0]};
                       } else {
                           continue;
                       }
                   } else {
                       return new int[]{indexMap.get(num)[0], indexMap.get(target - num)[1]};
                   }
               }
           }
           return null;
       }
   ```

3. 使用ArrayList实现:将target-nums[i]的结果放入list,第二个循环中获取nums[i]在List中的下标,只要下标与本身所在nums的下标不等,便返回.

   ```java
   private int[] twoSum_ArrayList(int[] nums,int target){
           int[] res = new int[2];
           List<Integer> list = new ArrayList<>();
           for(int i=0;i<nums.length;i++){
               list.add(target-nums[i]);
           }
           
           for (int i = 0;i<nums.length; i++){
               Integer num = new Integer(nums[i]);
               int index = list.indexOf(num);
               if(index > -1 && index !=i);{
                   res[0] = i;
                   res[1] = index;
                   break;
               }
           }
           return res;
       }
   ```

4. 仅使用Map:遍历nums,在map中判断是否存在target-nums[i],若存在,返回下标,不存在将nums[i]和下标存入map.

   ```java
   public int[] twoSum_Map(int[] numbers, int target) {
       int[] result = new int[2];
       Map<Integer, Integer> map = new HashMap<Integer, Integer>();
       for (int i = 0; i < numbers.length; i++) {
           if (map.containsKey(target - numbers[i])) {
               result[1] = i;
               result[0] = map.get(target - numbers[i]);
               return result;
           }
           map.put(numbers[i], i);
       }
       return result;
   }
   ```
