interface ChallengeType {
  id: number;
  title: string;
  preview_description: string;
  difficulty: string;
  completed: boolean;
  tag: string;
  flag: string;
}

const challenges: ChallengeType[] = [
  {
    id: 1,
    title: "Deleted, Not Gone",
    preview_description: "Found a public repo of an employee",
    difficulty: "EASY",
    completed: false,
    tag: "forensics",
    flag: "PT{d3l3t3d_n0t_g0n3_8f3a91c2}",
  },
  {
    id: 2,
    title: "Staging is Production",
    preview_description:
      "An admin-only endpoint trusts whatever role is in the JWT",
    difficulty: "MEDIUM",
    completed: false,
    tag: "web+crypto",
    flag: "PT{st4g1ng_1s_pr0ductn_r0le_tru5t_bug}",
  },
  {
    id: 3,
    title: "Inject, Not Vaccine",
    preview_description: "The login portal trusts whatever shape the query takes",
    difficulty: "MEDIUM",
    completed: false,
    tag: "nosqli",
    flag: "PT{n0sql_1nj3ct10n_byp4ss3d_4uth}",
  },
  {
    id: 4,
    title: "The Exfil Channel",
    preview_description: "One of these images is not like the others",
    difficulty: "MEDIUM",
    completed: false,
    tag: "stego",
    flag: "PT{st3g0_d4t4_hidd3n_1n_pl41n_s1ght}",
  },
  {
    id: 5,
    title: "Crack the Key",
    preview_description: "An internal tool guards a key behind a password check",
    difficulty: "MEDIUM",
    completed: false,
    tag: "reverse",
    flag: "PT{k3yg3n_p4ssw0rd_byp4ss3d}",
  },
  {
    id: 6,
    title: "The Nightly Backup",
    preview_description: "A backup job still runs over cleartext FTP",
    difficulty: "HARD",
    completed: false,
    tag: "network",
    flag: "PT{ftp_cl34rt3xt_cr3ds_s33n}",
  },
  {
    id: 7,
    title: "The Final Shell",
    preview_description: "A restricted account, one dangerous sudo rule",
    difficulty: "HARD",
    completed: false,
    tag: "linux",
    flag: "PT{tar_chkpt_r00t_esc4l4t10n}",
  },
];

export { challenges };
export type { ChallengeType };
