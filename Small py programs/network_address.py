""" Программа определяет, что полученные IP-адрес и маска являются правильными, а затем выводит адрес сети.
В случае, если IP-адрес или маска не верная – выводится "Валидация не пройдена" """

nums_ip = [int(i) for i in input().split('.')]
nums_mask = [int(i) for i in input().split('.')]


def mask_to_binary(nums):
    results = ''
    base = 2
    for num in nums:
        res = ''
        if not num:
            res = '0'
        else:
            while num > 0:
                res = str(num % base) + res
                num //= base
        if len(res) < 8:
            res = '0' * (8 - len(res)) + res
        if len(res) > 8:
            return False
        results += res
    return results


def mask_validation(nums):
    results = mask_to_binary(nums)
    if results:
        for i in range(1, len(results)):
            if results[i - 1] < results[i]:
                return False
        else:
            return True
    return False


def ip_validation(nums):
    if nums[0] == nums[1] == nums[2] == nums[3] == 0 or nums[0] == nums[1] == nums[2] == nums[3] == 255:
        return False
    for num in nums:
        if num < 0 or num > 255:
            return False
    return True


def net_address(nums1, nums2):
    res = []
    for i in range(4):
        res.append(str(nums1[i] & nums2[i]))
    return '.'.join(res)


if __name__ == "__main__":

    mask_check = mask_validation(nums_mask)
    ip_check = ip_validation(nums_ip)
    if mask_check and ip_check:
        print(net_address(nums_mask, nums_ip))
    else:
        print("Валидация не пройдена")
