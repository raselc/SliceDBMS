module Report where
import System.IO
import Data.List
--main fuction
main = do
        --location <- "SalesDB.slc"
        inh <- openFile "SalesDB.slc" ReadMode
        list <- getFile inh []
        hClose inh
        let a = ["Thank you"]
        let list2 = nub( map (deleteAll 2) list)
        x <- starter list2 list (length list2)
        print a
       
--deletes all element at a position
deleteAll _ [] = []
deleteAll x zs | x > 0 = take (x-1) zs ++ drop x zs
                | otherwise = zs
        
--deletes nth element from a list        
deleteElement n xs | n > 0 = take (n-1) xs ++ drop n xs

--prepares the id for the adder
starter lst1 lst2 len = 
        if len == 0
                then 
                        return "done"
                else do
                        let h = (head(head(lst1)))
                        let len2 = length lst2
                        y <-  adder h lst2 0.0 len2
                        let w = y
                        putStr ( h ++ " ")
                        print w
                        starter (tail lst1) lst2 (len-1)



--adds value of a specific order						
adder val lst total len =  
        if len == 0
                then do
                        return total
                else
                        if val == head(head lst)
                                then do
                                        let a =  head(tail(head lst))
                                        let b = map read $ words a ::[Float]
                                        --print (a)
                                        --print (b)
                                        --return total
                                        adder val (tail lst) (head b+total) (len-1)
                                else 
                                        --return total
                                        adder val (tail lst) total (len-1)
 
--reads from input file 
getFile inh lst = do 
        ineof <- hIsEOF inh
        if ineof
                then do
                        let finalList = reverse lst
                        return finalList
                else do 
                        inpStr <- hGetLine inh
                        let replacee = map (\c -> if c=='|' then ' ' else c)
                        let list1 = words ( replacee inpStr)
                        let list2 = deleteElement 1 list1
                        let list3 = deleteElement 2 list2
                        let list' = list3:lst
                        getFile inh list'  
