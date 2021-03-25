# LeetCode

## 605. 种花问题

[题目链接](https://leetcode-cn.com/problems/can-place-flowers/)
难度简单

假设你有一个很长的花坛，一部分地块种植了花，另一部分却没有。可是，花卉不能种植在相邻的地块上，它们会争夺水源，两者都会死去。

给定一个花坛（表示为一个数组包含0和1，其中0表示没种植花，1表示种植了花），和一个数 **n** 。能否在不打破种植规则的情况下种入 **n** 朵花？能则返回True，不能则返回False。

**示例 1:**

```
输入: flowerbed = [1,0,0,0,1], n = 1
输出: True
```

**示例 2:**

```
输入: flowerbed = [1,0,0,0,1], n = 2
输出: False
```

**注意:**

1.  数组内已种好的花不会违反种植规则。
2.  输入的数组长度范围为 [1, 20000]。
3.  **n** 是非负整数，且不会超过输入数组的大小。

我的解答：

判断前后是否符合要求

```c++
class Solution {
public:

    bool canPlant(vector<int>& flowerbed, int n){
        int l = flowerbed.size();
        if(n == 0)  return flowerbed[1] == 0;
        if(n == (l-1))  return flowerbed[l-2] == 0;
        return (flowerbed[n+1] == 0) && (flowerbed[n-1] == 0);
    }
    bool canPlaceFlowers(vector<int>& flowerbed, int n) {
        int cnt = 0;
        int l = flowerbed.size();
        if(l == 1){
            if(n > 1)  return false;
            else if(n == 1 && flowerbed[0] == 0)  return true;
            else if(n == 0)  return true;
            else  return false;
        }
        for(int i=0; i<l; i++){
            if(flowerbed[i] == 1)  continue;
            if(canPlant(flowerbed, i)){
                flowerbed[i] = 1;
                n--;
            }
        }

        return n <= 0;
    }
};
```



【1】当遍历到index遇到1时，说明这个位置有花，那必然从index+2的位置才有可能种花，因此当碰到1时直接跳过下一格。
【2】当遍历到index遇到0时，由于每次碰到1都是跳两格，因此前一格必定是0，此时只需要判断下一格是不是1即可得出index这一格能不能种花，如果能种则令n减一，然后这个位置就按照遇到1时处理，即跳两格；如果index的后一格是1，说明这个位置不能种花且之后两格也不可能种花（参照【1】），直接跳过3格。

当n减为0时，说明可以种入n朵花，则可以直接退出遍历返回true；如果遍历结束n没有减到0，说明最多种入的花的数量小于n，则返回false。

```c++
public boolean canPlaceFlowers(int[] flowerbed, int n) {
	for (int i = 0, len = flowerbed.length; i < len && n > 0;) {
		if (flowerbed[i] == 1) {
			i += 2;
		} else if (i == flowerbed.length - 1 || flowerbed[i + 1] == 0) {
			n--;
			i += 2;
		} else {
			i += 3;
		}
	}
	return n <= 0;
}
```

作者：hatsune-miku-k
链接：https://leetcode-cn.com/problems/can-place-flowers/solution/fei-chang-jian-dan-de-tiao-ge-zi-jie-fa-nhzwc/

## 239. 滑动窗口最大值
[题目链接](https://leetcode-cn.com/problems/sliding-window-maximum/)
给你一个整数数组 `nums`，有一个大小为 `k` 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。

返回滑动窗口中的最大值。

**示例 1：**

```
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```



思路：

窗口的最大值使用优先队列寻找，但是每当窗口向右移动，我们把刚刚进入窗口的元素加入堆中，同时判断最大的元素是否是已经被移出窗口，如果已经被移出窗口，我们就寻找下一个满足窗口左右区间的最大值

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int len = nums.length;
    if(k > len || k <= 0){
        return new int[0];
    }

    //大根堆，这里相当于 C++ 的 pair
    PriorityQueue<int[]> queue = new PriorityQueue<>( (o1, o2) -> o2[0] - o1[0]);
    int[] res = new int[len-k+1];

    int i = 0;
    for(; i<k; i++){
        queue.offer(new int[]{nums[i], i});
    }
    res[i-k] = queue.peek()[0];
    for(; i<len; i++){
        queue.add(new int[]{nums[i], i});
        while(queue.peek()[1] <= i-k){
            queue.poll();
        }
        res[i-k+1] = queue.peek()[0];
    }
    //这里也可以先判断最大值是否被移出堆，但是如果这样做就要判断堆是否为空
    //前面不需要判断的原因是，我们先把一个元素加入了堆，这个元素是肯定满足窗口左右区间的
    //所以堆一定不会为空，所以不需要判断
    //先判断最大值是否被移出堆的代码如下：
    /*
    for(; i<len; i++){
        while(!queue.isEmpty() && queue.peek()[1] <= i-k){
            queue.poll();
        }
        queue.add(new int[]{nums[i], i});
        res[i-k+1] = queue.peek()[0];
    }
    */

    return res;
}
```



```c++
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    int len = nums.size();
    if(k > len || k < 0)  return {};
    vector<int> res;

    int i = 0;
    priority_queue<pair<int, int>> q;//最大堆，存放数据和在数组中的位置
    for(; i<k; i++){
        q.emplace(nums[i], i);//原位构造元素，不产生临时对象
    }
    res.push_back(q.top().first);
    for(; i<len; i++){
        q.emplace(nums[i], i);//原位构造元素，不产生临时对象
        //判断最大值是否还在窗口内
        if(q.top().second <= i-k){
            q.pop();
        }
        res.push_back(q.top().first);
    }
    return res;
}
```



## 1232. 缀点成线
[题目链接](https://leetcode-cn.com/problems/check-if-it-is-a-straight-line/)难度简单

在一个 XY 坐标系中有一些点，我们用数组 `coordinates` 来分别记录它们的坐标，其中 `coordinates[i] = [x, y]` 表示横坐标为 `x`、纵坐标为 `y` 的点。

请你来判断，这些点是否在该坐标系中属于同一条直线上，是则返回 `true`，否则请返回 `false`。

 

**示例 1：**

![img](LeetCode.assets/untitled-diagram-2.jpg)

```
输入：coordinates = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]
输出：true
```

**示例 2：**

**![img](LeetCode.assets/untitled-diagram-1.jpg)**

```
输入：coordinates = [[1,1],[2,2],[3,4],[4,5],[5,6],[7,7]]
输出：false
```



**解答：**

求斜率可能遇到分母为 0 的情况，所以不用 $\ y=kx+b $ 的形式，用$\ \frac{y-y1}{x-x1} = \frac{y-y2}{x-x2} $   的变体 $\ (y-y1)*(x-x2)=(y-y2)*(x-x1) $

```java
class Solution {
    public boolean checkStraightLine(int[][] coordinates) {
        if(coordinates.length <= 2){
            return true;
        }

        int x1 = coordinates[0][0];
        int y1 = coordinates[0][1];

        int x2 = coordinates[1][0];
        int y2 = coordinates[1][1];

        for(int i=2; i<coordinates.length; i++){
            int x = coordinates[i][0];
            int y = coordinates[i][1];
            if((y-y1)*(x-x2) != (y-y2)*(x-x1)){
                return false;
            }
        }
        return true;
    }
}
```

