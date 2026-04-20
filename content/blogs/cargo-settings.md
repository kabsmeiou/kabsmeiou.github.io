# Cargo: Profiles and Settings

There are four types of profiles that come with default settings, if not explicitly defined. The settings can be defined/altered in Cargo.toml. The types are 'dev,' 'release,' 'test,' and 'bench.' It depends on the command whose profile is used to run it.

What follows are some of the settings that can be controlled in a profile:
- opt-level
- This is the optimization level where higher levels correspond to production of runtime code faster at the expense of slower compilation.
- Higher levels also change and rearrange the compiled code.
- 0 for no opt, 1 for basic opt, 2 for some opt, 3 for all opt, “s” to opt binary size, and “z” to opt binary size but turn off loop vectorization

I played with this setting using the minigrep project with the full Alice in Wonderland book and 100,000 lines of “the quick brown fox jumps over the lazy dog." The file big_alice.txt has exactly 103,384 lines. In my Cargo.toml, I added the following:

```rust
[profile.release-opt0]
inherits = "release"
opt-level = 0

[profile.release-opt1]
inherits = "release"
opt-level = 1

[profile.release-opt2]
inherits = "release"
opt-level = 2

[profile.release-opt3]
inherits = "release"
opt-level = 3

[profile.release-opts]
inherits = "release"
opt-level = "s"

[profile.release-optz]
inherits = "release"
opt-level = "z"
```
With these profiles, I compiled the code with the following commands:

```rust
cargo build --profile release-opt0                                                       
cargo build --profile release-opt1
cargo build --profile release-opt2
cargo build --profile release-opt3
cargo build --profile release-opts
cargo build --profile release-optz
```

Finally, to test, I used Hyperfine and ran the test with:

```bash
hyperfine \
'./target/release-opt0/minigrep the big_alice.txt' \
'./target/release-opt1/minigrep the big_alice.txt' \
'./target/release-opt2/minigrep the big_alice.txt' \
'./target/release-opt3/minigrep the big_alice.txt' \
'./target/release-opts/minigrep the big_alice.txt' \
'./target/release-optz/minigrep the big_alice.txt'
```

The results came out with opt-level = 3 being the fastest, recording 3.9 ms ± 0.2 ms. This is followed by opt-level = 2 with the same speed but with ±0.5 ms. The slowest setting was opt-level = 0 with 9.9 ms ± 0.4 ms. Meanwhile, opt-level = 2 and opt-level = “s” both recorded 4.5 ms, and opt-level = “z” resulted in 5.0 ms ± 0.6 ms.

Moving on from this setting, there is also a debug that controls the amount of debug information we can see included in the compiled binary. The valid options for this include:
- 0, false, or “none”
- “line-directives-only”
- “line-tables-only”
- 1 or “limited”
- 2, true, or “full”

Apparently, for release builds, it is conventional to set debug = 0 to keep the binaries small.

Then there’s also split-debuginfo, controlling where the generated debug information should appear (in the executable itself or adjacent to it). There is also a strip that tells rustc to strip symbols or debug info from a binary. Another debug-related setting is debug-assertions, which includes or excludes debug assertions that can be expensive or undesirable in a release build.

Different from the debug-related setting is the overflow-checks setting that allows us to control whether or not to include overflow checks that cause a panic once we encounter an overflow in the code. Aside from this, we can also control how panic behaves with “unwind” or “abort” strategies. Though depending on the platform, “abort” might be the only usable one, like the NVTPX platform. Additionally, tests, benchmarks, build scripts, and proc macros ignore this panic setting.