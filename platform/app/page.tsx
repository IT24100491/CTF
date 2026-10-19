"use client";

import Link from "next/link";
import { useChallenges } from "@/app/context/ChallengesProvider";
import { ChallengeType } from "@/app/libs/challenges";

const DIFFICULTY_STARS: Record<string, number> = {
  EASY: 1,
  MEDIUM: 3,
  HARD: 4,
  INSANE: 5,
};

function difficultyStars(difficulty: string) {
  const filled = DIFFICULTY_STARS[difficulty.toUpperCase()] ?? 1;
  return "*".repeat(filled) + ".".repeat(5 - filled);
}

export default function Home() {
  const { challenges, resetProgress } = useChallenges();
  const completedCount = challenges.filter((c) => c.completed).length;

  const handleReset = () => {
    if (
      window.confirm(
        "Reset all progress? This clears local storage and cannot be undone.",
      )
    ) {
      resetProgress();
    }
  };

  return (
    <div className="bg-black text-zinc-100 min-h-screen w-full overflow-x-hidden flex flex-col items-center font-mono selection:bg-zinc-100 selection:text-zinc-950 py-6 px-3 md:py-10">
      <div className="max-w-5xl w-full border border-zinc-800 rounded-md bg-zinc-950 shadow-[0_0_40px_rgba(0,0,0,0.6)] overflow-hidden flex flex-col">
        <div className="shrink-0 border-b border-zinc-800 bg-zinc-900/70 px-4 py-2.5 flex items-center gap-2">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
            <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
            <span className="w-2.5 h-2.5 rounded-full bg-green-500/70" />
          </div>
          <span className="flex-1 text-center text-[11px] text-zinc-500 tracking-wide truncate px-2">
            root@ctf: ~
          </span>
          <button
            onClick={handleReset}
            className="text-[10px] text-zinc-600 hover:text-red-400 border border-zinc-800 hover:border-red-900/60 px-2 py-0.5 transition-colors shrink-0"
          >
            rm -rf progress/
          </button>
        </div>

        <div className="p-4 md:p-6 text-xs leading-relaxed min-w-0">
          <p className="text-zinc-500">
            <span className="text-green-500">root@ctf</span>
            <span className="text-zinc-600">:</span>
            <span className="text-blue-400">~</span>
            <span className="text-zinc-600">$</span> cat /etc/briefing.txt
          </p>
          <div className="mt-2 mb-6 pl-0 space-y-3 text-zinc-400 border-l-2 border-zinc-800 pl-4">
            <p>
              We&apos;ve been hired by a private client to run an aggressive
              penetration test against a rival corporation. Word on the street
              is their developers cut corners, leaving their digital perimeter
              full of holes. Our objective is to infiltrate their staging
              infrastructure step-by-step, bypass their security controls, and
              extract what our client asked for before their team locks down the
              network.
            </p>
            <p className="text-zinc-500 italic">
              &gt; Complete each objective in order to progress. Good luck.
            </p>
          </div>

          <p className="text-zinc-500">
            <span className="text-green-500">root@ctf</span>
            <span className="text-zinc-600">:</span>
            <span className="text-blue-400">~</span>
            <span className="text-zinc-600">$</span> ls challenges/ --status
          </p>
          <div className="mt-2 mb-2 pl-4 flex items-center justify-between text-[11px] text-zinc-500">
            <span>
              {completedCount} / {challenges.length} objectives complete
            </span>
            <span className="text-zinc-600">
              {Math.round((completedCount / challenges.length) * 100)}%
            </span>
          </div>
          <div className="mb-6 pl-4 w-full h-1 bg-zinc-900">
            <div
              className="h-full bg-green-500/80 transition-all"
              style={{
                width: `${(completedCount / challenges.length) * 100}%`,
              }}
            />
          </div>

          <div className="pl-4 w-full grid grid-cols-1 md:grid-cols-3 gap-4 min-w-0">
            {challenges.map((challenge: ChallengeType, index: number) => {
              const isUnlocked =
                index === 0 || challenges[index - 1].completed;

              return (
                <div
                  key={challenge.id}
                  className={`border bg-black/60 p-4 flex flex-col justify-between gap-4 overflow-hidden relative group transition-colors min-w-0 ${
                    !isUnlocked
                      ? "border-zinc-900/40 opacity-40"
                      : challenge.completed
                        ? "border-zinc-300 shadow-[0_0_15px_rgba(255,255,255,0.05)]"
                        : "border-zinc-800 hover:border-zinc-600"
                  }`}
                >
                  <div className="min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <h1 className="text-sm font-semibold text-zinc-100 truncate">
                        {challenge.title.toLowerCase()}
                      </h1>
                      <span className="text-[10px] text-zinc-500 border border-zinc-800 px-1.5 py-0.5 shrink-0">
                        {challenge.tag.toLowerCase()}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[10px] mb-2">
                      <span className="text-zinc-600">
                        diff: {difficultyStars(challenge.difficulty)}
                      </span>
                      <span
                        className={`border px-1.5 py-0.5 ${
                          !isUnlocked
                            ? "border-zinc-800 text-zinc-700"
                            : challenge.completed
                              ? "border-emerald-900/60 text-emerald-400 bg-emerald-950/20"
                              : "border-orange-900/60 text-orange-400 bg-orange-950/20"
                        }`}
                      >
                        {!isUnlocked
                          ? "locked"
                          : challenge.completed
                            ? "solved"
                            : "unsolved"}
                      </span>
                    </div>
                    <p className="text-xs text-zinc-500 mb-2 wrap-break-words">
                      #{" "}
                      {isUnlocked
                        ? challenge.preview_description
                        : "Access denied. Complete the previous target to decrypt."}
                    </p>
                  </div>

                  {isUnlocked ? (
                    <Link
                      href={"challenges/" + challenge.id}
                      className="text-xs border border-zinc-700 text-zinc-200 hover:bg-zinc-900 hover:border-zinc-500 py-2 px-3 text-center transition-colors shrink-0"
                    >
                      cd challenges/{challenge.id}
                    </Link>
                  ) : (
                    <div className="text-xs border border-zinc-900 text-zinc-700 py-2 px-3 text-center cursor-not-allowed shrink-0">
                      locked
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <p className="mt-6 text-zinc-500">
            <span className="text-green-500">root@ctf</span>
            <span className="text-zinc-600">:</span>
            <span className="text-blue-400">~</span>
            <span className="text-zinc-600">$</span>{" "}
            <span className="inline-block w-2 h-3.5 bg-zinc-400 cursor-blink align-middle" />
          </p>
        </div>
      </div>
    </div>
  );
}
