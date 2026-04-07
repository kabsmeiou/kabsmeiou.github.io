# Closures in Rust

Rust has this thing called Closures and I find it pretty hard to understand. Regardless, I will try to explain here what it is so that when I forget about it at some point, I'll have something to review without going through the docs again.

### First of all, what exactly are closures?

When we say closures, think about normal functions but without a name. A function can have parameters, return values, and have some operation in the body. A closure is just like that. Consider the example below:

```rust
let closure_v1 = |num: u64| -> u64 { num + 5 };
```

In this specific example, we have a variable named `closure_v1` holding a closure that accepts a parameter `num` and adds 5 to it. It does the same thing as the named function below:

```rust
fn bump_value(num: u64) -> u64 { num + 5 }
```

Looks similar right? Not only that but they are doing the same thing, so why even use closures? Well, while closures can look like that, it can also be written like this:

```rust
let closure_v2 = |num| num + 5;
```

Cool, now it looks very compact! we made the code less verbose while still keeping the same level of readability. Is that the only thing it's for? No! It can be way more useful than that.

### Capturing values with closures

To emphasize its use case better, let's say we have the following code:

```rust
let bump_level = 10;
let closure_v3 = |num| num + bump_level;
// do something here
```

Looking at this code, we changed only one thing: instead of the constant 5, we use the `bump_level` variable instead. This makes the code easier to maintain and read in the long run.

Setting that aside, why is a closure a better choice here? Well, closures have what's called **capture**, and it means what it says: capturing a value outside of its scope. If this were a named function, we would also have to pass the `bump_level` variable:

```rust
fn bump_value(num: u64, bump_level: u64) -> u64 {
    num + bump_level
}
```

But with closures, there is no need to do that. A closure is able to carry context from the scope it is defined in, so whatever variable has been declared before it — as long as it's alive — the closure can use it.

### FnOnce, FnMut, and Fn

The examples I provided don't completely enumerate what's possible within a closure body, so I will list it down:

- We can move a captured value out of the closure
- We can mutate a captured value
- We can do neither of the above with the captured value (like in `closure_v3`)
- We can capture nothing at all (like in `closure_v1` and `closure_v2`)

I'm listing this down because knowing what a closure body does to what it has captured is important in understanding what traits it implements. Internally, closures will automatically implement one, two, or all three of the following traits: `FnOnce`, `FnMut`, and `Fn`. Let's go over them one by one.

---

**`FnOnce`** — it simply means that the closure can only be called once. This is implemented when we move the captured value out of the closure. For example:

```rust
let luka_doncic = String::from("ball");
let lebron_james = || luka_doncic;
```

`lebron_james` gets the ball once we call `lebron_james()`, moving the value `"ball"` out of `luka_doncic`. Because of this, we can't call `lebron_james()` again after calling it once — he already has the ball.

---

**`FnMut`** — the keyword here is *Mut* (mutation). It captures a value and mutates it. Using a similar context:

```rust
let mut luka_doncic = String::from("ball");
let mut lebron_james = || luka_doncic.push_str(" hog");
```

With this, no matter how many times we call `lebron_james()`, it will append `" hog"` to what `luka_doncic` is holding.

---

**`Fn`** — finally, this trait is implemented on closures that either capture nothing at all, or borrow a captured value without mutating it (read-only). Think of it as Lebron getting his own ball:

```rust
let luka_doncic = String::from("ball");
let lebron_james = || String::from("ball");
```

or `lebron_james` just referencing `luka_doncic`:

```rust
let luka_doncic = String::from("ball");
let lebron_james = || format!("{luka_doncic} pass me the ball!");
```

---

That's it! You've re-learned the basics of closures and can now use them again in your Rust code so try it out :)
