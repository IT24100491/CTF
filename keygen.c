/*
 * Veridian Analytics - Internal License/Key Utility
 * Stage 5 CTF challenge binary ("Crack the Key")
 *
 * Intended solve path: open in Ghidra/IDA Free, locate the
 * string-compare check in main/check_credentials, read the hardcoded
 * credential pair, or simply patch the conditional jump. Either
 * path reveals the hidden stage key below.
 *
 * Build on Windows:
 *   MSVC (Developer Command Prompt):
 *       cl keygen_windows.c /Fe:keygen.exe
 *
 *   MinGW / gcc:
 *       gcc -O2 -o keygen.exe keygen_windows.c
 */
#define _CRT_SECURE_NO_WARNINGS   /* silence MSVC "unsafe" warnings for fgets/strcmp */

#include <stdio.h>
#include <string.h>

/* Expected credentials for this internal tool */
static const char *EXPECTED_USER = "n.fernando";
static const char *EXPECTED_PASS = "V3r1d14n_1nt3rn4l_2024";

/* The second-stage key released after a successful check */
static const char *HIDDEN_KEY = "PT{k3yg3n_crack3d_r3v3rs3d_m3}";

static int check_credentials(const char *user, const char *pass) {
    if (strcmp(user, EXPECTED_USER) != 0) {
        return 0;
    }
    if (strcmp(pass, EXPECTED_PASS) != 0) {
        return 0;
    }
    return 1;
}

int main(void) {
    char username[128];
    char password[128];

    printf("=== Veridian Analytics Internal Keygen Utility v1.2 ===\n");
    printf("Username: ");
    if (!fgets(username, sizeof(username), stdin)) {
        return 1;
    }
    username[strcspn(username, "\r\n")] = '\0';

    printf("Password: ");
    if (!fgets(password, sizeof(password), stdin)) {
        return 1;
    }
    password[strcspn(password, "\r\n")] = '\0';

    if (check_credentials(username, password)) {
        printf("\n[+] Access granted.\n");
        printf("[+] Encryption key: %s\n", HIDDEN_KEY);
        return 0;
    } else {
        printf("\n[-] Access denied. Invalid credentials.\n");
        return 1;
    }
}
