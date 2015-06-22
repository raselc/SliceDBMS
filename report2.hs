module Report2 where
import System.IO
import Data.List

--main fucntion
main = do
        inh <- openFile "CustDB.slc" ReadMode
        clist <- getCustFile inh []
        hClose inh
        
        inh1 <- openFile "SalesDB.slc" ReadMode
        salesDB <- getSalesFile inh1 []
        hClose inh1
        
        inh2 <- openFile "OrderDB.slc" ReadMode
        orderDB <- getOrderFile inh2 []
        hClose inh2
                
        semiFinal <- ageFinder clist [] (length clist)
        custDB <- deleteAge semiFinal [] (length semiFinal)
        salesFinder custDB (length custDB) salesDB orderDB
        print("done")
        

--prepares the customer id for the next fuction		
salesFinder cusList len salesDB orderDB= do
        --print list
        if len == 0
                then do
                        return "--"
                else do
                        let h = head (head cusList)
                        let name = head(tail (head cusList))
                        --print h
                        --print name
                        y <- orderFinder name h salesDB (length salesDB) orderDB 
                        salesFinder (tail cusList) (len-1) salesDB orderDB

--it takes a customer id, SalesDB, a list length of salesdb
orderFinder name cus olist len orderDB= do
       -- print list
        if len == 0
                then do
                        --print (len)
                        return "---"
                else do
                        if cus == head (tail (head (olist)))
                                then do
                                        --print (head (head olist))
                                        val <- itemFinder (head (head olist)) orderDB [] (length orderDB)
                                        let orderNumber = (head (head olist))
                                        let date = (last (head olist))
                                        putStrLn (name++" "++orderNumber ++" " ++ " "++ date++" " ++unwords(val))
                                        --print (val)
                                        orderFinder name cus (tail olist) (len-1) orderDB                                         
                                        
                                else
                                        orderFinder name cus (tail olist) (len-1) orderDB
                        
--finds the item with a specific order number
itemFinder oNum list rList len=
        if len == 0
                then do
                        let fList = reverse rList
                        return fList
                else do
                        if oNum == head (head list)
                                then do
                                        let t = head (tail (head list))
                                        --print t
                                        let list' =t:rList
                                        --print list'
                                        itemFinder oNum (tail list) list' (len-1)
                                else
                                        itemFinder oNum (tail list) rList (len-1)
                                        --return 3
                                                        
                
--deletes nth element of a list
deleteElement n xs | n > 0 = take (n-1) xs ++ drop n xs

--returns a list where customer is >= 60
ageFinder custList nList len = do
        if len == 0
                then do
                        let rList = reverse nList
                        return rList
                else do
                        if last(head custList) > "59"
                                then do
                                        let temp = (head custList):nList
                                        ageFinder (tail custList) temp (len-1)
                                else
                                        ageFinder (tail custList) nList (len-1)

--deletes age column from customer database
deleteAge custList nList len = do
        if len == 0
                then do
                        let rList = reverse nList
                        return rList
                else do
                        let temp = deleteElement 3 (head custList)
                        let list' = temp:nList
                        deleteAge (tail custList) list' (len-1)

--reads order database file
getOrderFile inh lst = do 
        ineof <- hIsEOF inh
        if ineof
                then do
                        let finalList = reverse lst
                        return finalList
                else do 
                        inpStr <- hGetLine inh
                        let replacee = map (\c -> if c=='|' then ' ' else c)
                        let list1 = words ( replacee inpStr)
                        let list' = list1:lst
                        getOrderFile inh list'

--reads sales database file						
getSalesFile inh lst = do 
        ineof <- hIsEOF inh
        if ineof
                then do
                        let finalList = reverse lst
                        return finalList
                else do 
                        inpStr <- hGetLine inh
                        let replacee = map (\c -> if c=='|' then ' ' else c)
                        let list1 = words ( replacee inpStr)
                        let list3 = deleteElement 4 list1
                        let list' = list3:lst
                        getSalesFile inh list'

--reads customer database file                        
getCustFile inh lst = do 
        ineof <- hIsEOF inh
        if ineof
                then do
                        let finalList = reverse lst
                        return finalList
                else do 
                        inpStr <- hGetLine inh
                        let replaceS = map (\c -> if c==' ' then '_' else c)
                        let replaceD = map (\c -> if c=='|' then ' ' else c)
                        let list1 = words (replaceD( replaceS inpStr))
                        let list2 = deleteElement 5 list1
                        let list3 = deleteElement 4 list2
                        let list' = list3:lst
                        getCustFile inh list'
