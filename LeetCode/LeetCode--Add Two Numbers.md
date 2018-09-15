## Add Two Numbers ##

### Question ###

You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order** and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.



### Example ###

```java
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.
```

### Solution ###

1. 暴力撸即可,依次遍历相加,可通过 /10 将高位加到下一位.

   ```java
   private ListNode addTwoNumber2(ListNode l1, ListNode l2) {
           ListNode prev = new ListNode(0);
           ListNode head = prev;
           int cur = 0;
   
           while (l1 != null || l2 != null || cur != 0) {
               int sum = ((l1 == null) ? 0 : l1.val) + ((l2 == null) ? 0 : l2.val) + cur;
               cur = sum / 10;
               prev.next = new ListNode(sum % 10);
               prev = prev.next;
   
               l1 = (l1 != null) ? l1.next : l1;
               l2 = (l2 != null) ? l2.next : l2;
           }
           return head.next;
       }
   ```
