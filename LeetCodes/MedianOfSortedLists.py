def findMedianSortedArrays(nums1, nums2):
    """
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: float
    """
    length1 = len(nums1)
    length2 = len(nums2)

    if length1 == length2:
        nums1.extend(nums2)
        nums1.sort()
        print(nums1)
        newListLength = len(nums1)
        median = (nums1[newListLength//2] + nums1[(newListLength//2)-1]) / 2
    else:
        nums1.extend(nums2)
        nums1.sort()
        print(nums1)
        newListLength = len(nums1)
        if len(nums1) % 2 == 0:
            median = (nums1[newListLength//2] + nums1[(newListLength//2)-1]) / 2
        else:
            median = nums1[int((newListLength/2)-0.5)]
    return median

nums1 = [1, 2]
nums2 = [3, 4, 7]

print(findMedianSortedArrays(nums1, nums2))
