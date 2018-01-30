import qualified Data.Map as M
import Data.Maybe
import System.IO

type State = Int
type States = [State]
type Symbol = Char
type Alphabet = [Symbol]
type Transition = ((State, Symbol), State)
type Transitions = [Transition]

data DFA = DFA { states :: States
               , alphabet :: Alphabet
               , transitions :: Transitions 
               , start :: State 
               , finals :: States 
               } deriving (Show)

main :: IO ()
main = do
    let table = [((0, '0'), 0), ((0, '1'), 1)
                ,((1, '0'), 0), ((1, '1'), 1)
                ] :: Transitions
        simpleDFA = DFA [0,1] "01" table 0 [0] :: DFA
    putStr "Enter word >>> "
    hFlush stdout
    input <- getLine
    putStrLn $ show $ simulate simpleDFA (start simpleDFA) input

move :: DFA -> (State, Symbol) -> State
move dfa pair = fromJust $ M.lookup pair (M.fromList $ transitions dfa) 

simulate :: DFA -> State -> String -> Bool
simulate dfa state input
    | input == "" = state `elem` (finals dfa)
    | otherwise   = simulate dfa (move dfa (state, c)) cs
    where c = head input
          cs = tail input

