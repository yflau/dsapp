#! /usr/bin/env python
#coding: utf-8

"""
1 ����˵��
�� ʹ�ö����������� test file�а��������е��ʵķ���Ƶ����
�� ʹ�ö��������ʱ�����������keyword��˳�� tree����ƫб������б��д����ֹ������������㷨��
2 ����
�� ������ļ����ƣ� data.txt
�ļ�������δ֪��ʹ�ó��������еĻ��۷�
�� ����ļ����ƣ� output.txt
�� Data.txt�ļ�Ϊ���ű��� webpage ��һ���test �ļ�
�C�����ļ������ĵ����ڶ�������������
�Cͬһ�����ʶ�γ��ֵ��������¼��������
�C���ʲ��ִ�Сд
�Cɾ���Լ���֪�������ַ���(. , �� ��? ! : ��)
�C�ļ���������ĺ�����fopen������fgets������ʹ�ã����ʵĻ���ʹ��strtok��������
3 ���
�� ����ļ�����Ҫ���������
�C���ʣ����ʵķ���Ƶ����
�C��˳��������ʵ�������ĸ
�� ��������������
"""

"""
Even though the bounty is gone, since the accepted answer gives the extremely-false impression that binary-trees are not very useful, I will post another answer.

To squabble about the performance of binary-trees is meaningless - they are not a data structure, but a family of data structures, all with different performance characteristics. While it is true that unbalanced binary trees perform much worse than self-balancing binary trees for searching, there are many binary trees (such as binary tries) for which "balancing" has no meaning.
Applications of binary trees

    Binary Search Tree - Used in many search applications where data is constantly entering/leaving, such as the map and set objects in many languages' libraries.
    Binary Space Partition - Used in almost every 3D video game to determine what objects need to be rendered.
    Binary Tries - Used in almost every high-bandwidth router for storing router-tables.
    Hash Trees - used in p2p programs and specialized image-signatures in which a hash needs to be verified, but the whole file is not available.
    Heaps - Used in implementing efficient priority-queues, which in turn are used for scheduling processes in many operating systems, Quality-of-Service in routers, and A* (path-finding algorithm used in AI applications, including robotics and video games). Also used in heap-sort.
    Huffman Coding Tree (Chip Uni) - used in compression algorithms, such as those used by the .jpeg and .mp3 file-formats.
    GGM Trees - Used in cryptographic applications to generate a tree of pseudo-random numbers.
    Syntax Tree - Constructed by compilers and (implicitly) calculators to parse expressions.
    Treap - Randomized data structure used in wireless networking and memory allocation.
    T-tree - Though most databases use some form of B-tree to store data on the drive, databases which keep all (most) their data in memory often use T-trees to do so.

The reason that binary trees are used more often than n-ary trees for searching is that n-ary trees are more complex, but usually provide no real speed advantage.

In a (balanced) binary tree with m nodes, moving from one level to the next requires one comparison, and there are log_2(m) levels, for a total of log_2(m) comparisons.

In contrast, an n-ary tree will it will require log_2(n) comparisons (using a binary search) to move to the next level. Since there are log_n(m) total levels, the search will require log_2(n)*log_n(m) = log_2(m) comparisons total. So, though n-ary trees are more complex, they provide no advantage in terms of total comparisons necessary.

(However, n-ary trees are still useful in niche-situations. The examples that come immediately to mind are quad-trees and other space-partitioning trees, where divisioning space using only two nodes per level would make the logic unnecessarily complex; and B-trees used in many databases, where the limiting factor is not how many comparisons are done are each level but how many nodes can be loaded from the hard-drive at once)

"""

