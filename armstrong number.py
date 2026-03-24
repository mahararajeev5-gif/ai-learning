n=int(input("enter your no : "))
sum=0
order=len(str(n))
copy_n=n
while(n>0):
    digit=n%10
    sum +=digit**order
    n=n//10

if sum==copy_n:
        print(" armstrong number")

else:
    print("not a armstrong number")