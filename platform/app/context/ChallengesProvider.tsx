"use client";
import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import {
  challenges as initialChallenges,
  type ChallengeType,
} from "@/app/libs/challenges";

interface ChallengesContextType {
  challenges: ChallengeType[];
  completeChallenge: (id: number) => void;
  resetProgress: () => void;
  isLoaded: boolean;
}

const ChallengesContext = createContext<ChallengesContextType | undefined>(
  undefined,
);

const STORAGE_KEY = "challenges-progress";

export function ChallengesProvider({ children }: { children: ReactNode }) {
  // Same value on server AND on first client render -> no mismatch
  const [challenges, setChallenges] =
    useState<ChallengeType[]>(initialChallenges);
  const [isLoaded, setIsLoaded] = useState(false);

  // Runs only on the client, after hydration - safe to touch localStorage here
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const savedChallenges: ChallengeType[] = JSON.parse(saved);
        setChallenges((current) =>
          current.map((challenge) => {
            const match = savedChallenges.find((s) => s.id === challenge.id);
            return match
              ? { ...challenge, completed: match.completed }
              : challenge;
          }),
        );
      }
    } catch (error) {
      console.error("Failed to load challenges from localStorage:", error);
    } finally {
      setIsLoaded(true);
    }
  }, []);

  // Persist whenever challenges change (skip the very first render before load)
  useEffect(() => {
    if (!isLoaded) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(challenges));
    } catch (error) {
      console.error("Failed to save challenges to localStorage:", error);
    }
  }, [challenges, isLoaded]);

  const completeChallenge = (id: number) => {
    setChallenges((current) =>
      current.map((challenge) =>
        challenge.id === id ? { ...challenge, completed: true } : challenge,
      ),
    );
  };

  const resetProgress = () => {
    try {
      localStorage.clear();
    } catch (error) {
      console.error("Failed to clear localStorage:", error);
    }
    setChallenges(initialChallenges);
  };

  return (
    <ChallengesContext.Provider
      value={{
        challenges,
        completeChallenge,
        resetProgress,
        isLoaded,
      }}
    >
      {children}
    </ChallengesContext.Provider>
  );
}

export function useChallenges() {
  const context = useContext(ChallengesContext);
  if (context === undefined) {
    throw new Error("useChallenges must be used inside ChallengesProvider");
  }
  return context;
}
