## Longest Substring Without Repeating Characters ##

### Question ###

Given a string, find the length of the **longest substring** without repeating characters.



### Example ###

**Example 1:**

```
Input: "abcabcbb"
Output: 3 
Explanation: The answer is "abc", with the length of 3. 
```

**Example 2:**

```
Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**

```
Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. 
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
```



### Solution ###

1. 暴力撸.从第一个字符开始遍历,同时计数,若遍历到相同字符,从此重新遍历,并重新计数,比较两次计数大小,直至遍历结束,取最大数.