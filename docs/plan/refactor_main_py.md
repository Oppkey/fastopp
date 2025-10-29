# Refactor main.py: Extract Non-Essential Logic

**Date**: 2025-10-29

**⚠️ Prerequisite**: This plan should be executed **after** completing the `move_base_to_dependency_injection.md` plan. The dependency injection plan establishes foundational patterns that should be in place before refactoring.

## Analysis Summary

The `main.py` file contains several concerns that should be extracted:

1. **Admin customization logic** (lines 122-315): Font file routes, CSS redirects, and FontAwesome injection middleware (~194 lines)
2. **General middleware** (lines 61-71): Proxy headers middleware (~11 lines)
3. **Exception handlers** (lines 332-364): HTTP and global exception handlers (~33 lines)
4. **Setup functions** (lines 75-91): Dependency setup function (~17 lines)
5. **Static file mounting** (lines 93-104): Static file configuration logic (~12 lines)
6. **Favicon route** (lines 157-163): Simple favicon handler (~7 lines)

## Comparison: root main.py vs base_assets/main.py

**Key Differences Found:**

| Feature                         | Root main.py (Current)                                    | base_assets/main.py           |
| ------------------------------- | --------------------------------------------------------- | ----------------------------- |
| **Dependency Injection**        | ✅ Yes (`dependencies.database`, `dependencies.config`)   | ❌ No (direct imports)        |
| **Storage System**              | ✅ Yes (`core.services.storage`)                          | ❌ No                         |
| **Proxy Headers Middleware**    | ✅ Yes                                                    | ❌ No                         |
| **Dependency Setup Function**   | ✅ Yes (`setup_dependencies()`)                           | ❌ No                         |
| **Routers**                     | ✅ Multiple (chat, api, health, webinar, oppdemo, oppman) | ❌ Only (auth, pages, oppman) |
| **Exception Handlers**          | ✅ Advanced (global + database health check)              | ❌ Basic only                 |
| **Template Context Processors** | ✅ Yes (`core.services.template_context`)                 | ❌ No                         |
| **Static File Mounting**        | ✅ Environment-aware                                      | ❌ Basic                      |
| **FontAwesome Customization**   | ✅ Yes (duplicated code)                                  | ✅ Yes (duplicated code)      |
| **Lines of Code**               | ~365 lines                                                | ~276 lines                    |

**Conclusion**: The root `main.py` is significantly more advanced with dependency injection, better error handling, and more features. Replacing it with `base_assets/main.py` during destroy operations would lose all these improvements.

## Proposed File Organization

**Important**: Do NOT use `admin/` directory - it gets replaced during cleanup operations. Use `core/` instead.

### 1. `core/middleware/admin.py` ✅ SAFE

- Font file route handler (serve_font_files)
- FontAwesome CSS redirect route (fontawesome_css_redirect)
- FontAwesome injection middleware (inject_fontawesome_cdn)
- Function: `register_admin_middleware(app: FastAPI)`

### 2. `core/middleware/proxy.py`

- Proxy headers middleware function: `create_proxy_headers_middleware()`
- Function: `register_proxy_headers_middleware(app: FastAPI)`

### 3. `core/middleware/__init__.py`

- Export middleware registration functions
- Create new `core/middleware/` directory

### 4. `core/exceptions.py`

- HTTP exception handler
- Global exception handler
- Function: `register_exception_handlers(app: FastAPI)`

### 5. `core/setup.py`

- `setup_dependencies(app: FastAPI, settings)` function
- `setup_static_files(app: FastAPI, settings)` function
- `setup_templates()` function (returns Jinja2Templates instance)

### 6. `routes/static.py` (optional)

- Favicon route handler
- Function: `register_static_routes(app: FastAPI)`
- **Alternative**: Keep favicon in `routes/pages.py` if preferred

## Implementation Steps

1. Create `core/middleware/` directory with `__init__.py`
2. Create `core/middleware/admin.py` with admin customization code
3. Create `core/middleware/proxy.py` with proxy headers middleware
4. Create `core/exceptions.py` for exception handlers
5. Create `core/setup.py` for setup functions
6. Create `routes/static.py` for favicon route (or move to pages.py)
7. Update root `main.py` to import and call registration functions
8. Verify all imports and functionality work correctly

## Benefits

- `main.py` becomes focused on app initialization and router registration
- Related functionality grouped logically in `core/` (safe from cleanup)
- Easier to test individual components
- Better separation of concerns
- Consistent with existing project structure (`core/services/`, `routes/`)

## Important Notes

- **DO NOT** use `admin/` directory for new files - it gets replaced during `oppdemo.py destroy`
- `core/` directory is safe from cleanup operations
- After extraction, consider updating `oppdemo.py destroy` to preserve the improved `main.py` or update `base_assets/main.py` to match the dependency injection approach

## Important Findings

### Admin Directory Behavior

1. ✅ `oppman.py clean` does NOT directly target `admin/` in its cleanup list
2. ❌ `oppdemo.py destroy` REPLACES the entire `admin/` directory with `base_assets/admin/`
3. ❌ `oppman.py clean` indirectly affects `admin/` because it calls `oppdemo.py destroy` first
4. ✅ `core/` directory is NOT affected by cleanup operations

**Conclusion**: Any new files added to `admin/` would be lost during cleanup. Using `core/middleware/admin.py` ensures the code persists across cleanup operations.

### main.py Replacement Issue

- Root `main.py` uses advanced dependency injection and has ~365 lines
- `base_assets/main.py` is a minimal version (~276 lines) without dependency injection
- When `oppdemo.py destroy` runs, it replaces the advanced root `main.py` with the minimal version
- **Recommendation**: Consider removing `main.py` from the destroy command, or ensure `base_assets/main.py` includes dependency injection support
