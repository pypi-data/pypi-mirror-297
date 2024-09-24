#include "api.h"
#include "license_api.h"
#include <memory>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <unordered_map>

#include <map>
#include <pybind11/operators.h>
#include <sstream>

class PyEventHandler : public EventHandler {
public:
  using EventHandler::EventHandler;

  void handle(Model &model, SolverEvent event) override {
    PYBIND11_OVERRIDE_PURE(void,         // 返回类型
                           EventHandler, // 父类
                           handle,       // 函数名
                           model,        // 参数
                           event);
  }
};

// Here, you should include all the necessary header files for your classes

// You can create a specific namespace to avoid conflicts
namespace py = pybind11;

PYBIND11_MODULE(pyseedmip,
                m) { // replace 'your_module_name' with your actual module name
  // Binding for the License class
  py::class_<License>(m, "License")
      .def(py::init<>())
      .def("activate", &License::activate);

  // Binding for constants
  m.attr("DEFAULT_LB") = DEFAULT_LB;
  m.attr("DEFAULT_UB") = DEFAULT_UB;

  // Binding for VType enum
  py::enum_<VType>(m, "VType")
      .value("BINARY", VType::BINARY)
      .value("INTEGER", VType::INTEGER)
      .value("REAL", VType::REAL)
      .export_values();

  // Binding for SolverEvent enum
  py::enum_<SolverEvent>(m, "SolverEvent")
      .value("START_SOLVING", SolverEvent::START_SOLVING)
      .value("NEW_SOL_FOUND", SolverEvent::NEW_SOL_FOUND)
      .value("BEST_SOL_FOUND", SolverEvent::BEST_SOL_FOUND)
      .value("INTERUPTED", SolverEvent::INTERUPTED)
      .value("SOLVING_END", SolverEvent::SOLVING_END)
      .export_values();

  // Binding for Status enum
  py::enum_<Status>(m, "Status")
      .value("INITIAL_STATE", Status::INITIAL_STATE)
      .value("START_SOLVING", Status::START_SOLVING)
      .value("NEW_SOL_FOUND", Status::NEW_SOL_FOUND)
      .value("BEST_SOL_FOUND", Status::BEST_SOL_FOUND)
      .value("INTERUPTED", Status::INTERUPTED)
      .value("SOLVING_END", Status::SOLVING_END)
      .export_values();

  // Binding for SolStatus enum
  py::enum_<SolStatus>(m, "SolStatus")
      .value("SOL_NOT_FOUND", SolStatus::SOL_NOT_FOUND)
      .value("SOL_FOUND", SolStatus::SOL_FOUND)
      .export_values();

  // Binding for Env class
  py::class_<Env>(m, "Env")
      .def(py::init<>())
      .def("getCutoff", &Env::getCutoff)
      .def("setCutoff", &Env::setCutoff);

  py::class_<TempConstr>(m, "TempConstr")
      .def(py::init<>())
      .def(py::init<const TempConstr &>())
      .def("assign", &TempConstr::operator=);

  // Binding for Var class
  py::class_<Var, std::shared_ptr<Var>>(m, "Var")
      //.def(py::init<>())
      //.def(py::init<const std::string &>())
      //.def("setDict", &Var::setDict)

      .def("getIsFix", &Var::getIsFix)
      .def("fix", &Var::fix)
      .def("unfix", &Var::unfix)
      .def("getUserValue", &Var::getUserValue)
      .def("setUserValue", &Var::setUserValue)
      .def("getName", &Var::getName)
      .def("getVal", &Var::getVal)
      .def("setName", &Var::setName)
      .def("setVal", &Var::setVal)
      .def("getType", &Var::getType)
      .def("setType", &Var::setType)
      .def("setUB", &Var::setUB)
      .def("getUB", &Var::getUB)
      .def("setLB", &Var::setLB)
      .def("getLB", &Var::getLB)
      .def("sameAs", &Var::sameAs)
      //    .def("__eq__", &Var::operator==)
      .def("__lt__", &Var::operator<)

      .def(
          "__le__",
          [](const Var &x, const Var &y) -> TempConstr {
            return LinExpr(x) <= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__le__",
          [](const Var &x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) <= y;
          },
          py::is_operator())
      .def(
          "__le__",
          [](const Var &x, const double &y) -> TempConstr {
            return LinExpr(x) <= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__le__",
          [](const LinExpr &x, const Var &y) -> TempConstr {
            return x <= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__le__",
          [](const double x, const Var &y) -> TempConstr {
            return LinExpr(x) <= LinExpr(y);
          },
          py::is_operator())

      .def(
          "__ge__",
          [](const Var &x, const Var &y) -> TempConstr {
            return LinExpr(x) >= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const Var &x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) >= y;
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const Var &x, const double &y) -> TempConstr {
            return LinExpr(x) >= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const LinExpr &x, const Var &y) -> TempConstr {
            return x >= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const double x, const Var &y) -> TempConstr {
            return LinExpr(x) >= LinExpr(y);
          },
          py::is_operator())

      .def(
          "__eq__",
          [](const Var &x, const Var &y) -> TempConstr {
            return LinExpr(x) == LinExpr(y);
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const Var &x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) == y;
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const Var &x, const double &y) -> TempConstr {
            return LinExpr(x) == LinExpr(y);
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const LinExpr &x, const Var &y) -> TempConstr {
            return x == LinExpr(y);
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const double x, const Var &y) -> TempConstr {
            return LinExpr(x) == LinExpr(y);
          },
          py::is_operator())

      // 加法运算符重载
      .def(
          "__add__",
          [](const Var &v1, const Var &v2) -> LinExpr {
            return LinExpr(v1) + LinExpr(v2);
          },
          py::is_operator())
      .def(
          "__add__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            return LinExpr(v) + e;
          },
          py::is_operator())
      .def(
          "__add__",
          [](const Var &v, const double d) -> LinExpr {
            return LinExpr(v) + d;
          },
          py::is_operator())
      .def(
          "__radd__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            return e + LinExpr(v);
          },
          py::is_operator())
      .def(
          "__radd__",
          [](const Var &v, const double d) -> LinExpr {
            return d + LinExpr(v);
          },
          py::is_operator())

      // 减法运算符重载
      .def(
          "__sub__",
          [](const Var &v1, const Var &v2) -> LinExpr {
            return LinExpr(v1) - LinExpr(v2);
          },
          py::is_operator())
      .def(
          "__sub__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            return LinExpr(v) - e;
          },
          py::is_operator())
      .def(
          "__sub__",
          [](const Var &v, const double d) -> LinExpr {
            return LinExpr(v) - d;
          },
          py::is_operator())
      .def(
          "__rsub__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            return e - LinExpr(v);
          },
          py::is_operator())
      .def(
          "__rsub__",
          [](const Var &v, const double d) -> LinExpr {
            return d - LinExpr(v);
          },
          py::is_operator())

      // 乘法和除法运算符重载（只需处理与 double 的操作）
      .def(
          "__mul__",
          [](const Var &v, const double d) -> LinExpr {
            return LinExpr(v) * d;
          },
          py::is_operator())
      .def(
          "__rmul__",
          [](const Var &v, const double d) -> LinExpr {
            return d * LinExpr(v);
          },
          py::is_operator())
      .def(
          "__truediv__",
          [](const Var &v, const double d) -> LinExpr {
            return LinExpr(v) / d;
          },
          py::is_operator())

      // in-place 运算符重载
      .def(
          "__iadd__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            LinExpr temp = LinExpr(v);
            temp += e;
            return temp;
          },
          py::is_operator())
      .def(
          "__isub__",
          [](const Var &v, const LinExpr &e) -> LinExpr {
            LinExpr temp = LinExpr(v);
            temp -= e;
            return temp;
          },
          py::is_operator())
      .def(
          "__imul__",
          [](const Var &v, const double d) -> LinExpr {
            LinExpr temp = LinExpr(v);
            temp *= d;
            return temp;
          },
          py::is_operator())
      .def(
          "__itruediv__",
          [](const Var &v, const double d) -> LinExpr {
            LinExpr temp = LinExpr(v);
            temp /= d;
            return temp;
          },
          py::is_operator())
      .def(
          "__pos__", [](const Var &v) -> LinExpr { return +LinExpr(v); },
          py::is_operator())

      // 负运算符重载
      .def(
          "__neg__", [](const Var &v) -> LinExpr { return -LinExpr(v); },
          py::is_operator());
  ;

  // Binding for the Constr class
  py::class_<Constr>(m, "Constr")
      //.def(py::init<>())
      //.def(py::init<const std::vector<Var> &, const std::vector<double> &,
      //              const std::string &, double, const std::string &>())
      .def("getName", &Constr::getName)
      .def("getSense", &Constr::getSense)
      .def("getRhs", &Constr::getRhs)
      .def("setRhs", &Constr::setRhs)
      .def("getVarList", &Constr::getVarList)
      .def("getCoeffList", &Constr::getCoeffList)
      .def("setName", &Constr::setName)
      .def("setSense", &Constr::setSense)
      //.def("setVarList", &Constr::setVarList)
      //.def("setCoeffList", &Constr::setCoeffList)
      //.def("pushBackVarList", &Constr::pushBackVarList)
      //.def("pushBackCoeffList", &Constr::pushBackCoeffList)
      //.def("setDict", &Constr::setDict)
      .def("chgCoeff", &Constr::chgCoeff)
      .def("getCoeff", &Constr::getCoeff)
      .def("chgCoeffs", &Constr::chgCoeffs)
      .def("sameAs", &Constr::sameAs);

  py::class_<LinExpr, std::shared_ptr<LinExpr>>(m, "LinExpr")
      .def(py::init<>())
      .def(py::init<const double>(), py::arg("constant") = 0.0)
      .def(py::init<const Var &, const double>(), py::arg("var"),
           py::arg("coeff") = 1.0)
      .def("add", &LinExpr::add)
      .def("addConstant", &LinExpr::addConstant)
      .def("addTerms", &LinExpr::addTerms)
      .def("clear", &LinExpr::clear)
      .def("getConstant", &LinExpr::getConstant)
      //.def("getCoeff", &LinExpr::getCoeff)
      .def("getCoeff", (double (LinExpr::*)(int) const)&LinExpr::getCoeff)
      .def("getCoeff", (double (LinExpr::*)(const Var&) const) &LinExpr::getCoeff)
      .def("getValue", &LinExpr::getValue)
      .def("getVar", &LinExpr::getVar)
      .def("remove_by_inx", (void(LinExpr::*)(const int)) & LinExpr::remove)
      .def("remove_by_var", (void(LinExpr::*)(const Var &)) & LinExpr::remove)
      .def("size", &LinExpr::size)
      .def("__repr__",
           [](const LinExpr &a) {
             std::ostringstream os;
             os << a;
             return os.str();
           })
      .def("__iadd__", &LinExpr::operator+=, py::is_operator())
      .def("__isub__", &LinExpr::operator-=, py::is_operator())
      .def("__imul__", &LinExpr::operator*=, py::is_operator())
      .def("__itruediv__", &LinExpr::operator/=, py::is_operator())
      .def(py::self + py::self)
      .def(+py::self)
      .def(py::self + double())
      .def(double() + py::self)
      .def(py::self - py::self)
      .def(-py::self)
      .def(py::self - double())
      .def(double() - py::self)
      .def(py::self * double())
      .def(double() * py::self)
      .def(py::self / double())

      .def(
          "__le__",
          [](const LinExpr &x, const LinExpr &y) -> TempConstr {
            return x <= y;
          },
          py::is_operator())
      .def(
          "__le__",
          [](const LinExpr &x, const double y) -> TempConstr {
            return x <= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__le__",
          [](const double x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) <= y;
          },
          py::is_operator())

      .def(
          "__ge__",
          [](const LinExpr &x, const LinExpr &y) -> TempConstr {
            return x >= y;
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const LinExpr &x, const double y) -> TempConstr {
            return x >= LinExpr(y);
          },
          py::is_operator())
      .def(
          "__ge__",
          [](const double x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) >= y;
          },
          py::is_operator())

      .def(
          "__eq__",
          [](const LinExpr &x, const LinExpr &y) -> TempConstr {
            return x == y;
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const LinExpr &x, const double y) -> TempConstr {
            return x == LinExpr(y);
          },
          py::is_operator())
      .def(
          "__eq__",
          [](const double x, const LinExpr &y) -> TempConstr {
            return LinExpr(x) == y;
          },
          py::is_operator());

  py::implicitly_convertible<double, LinExpr>();
  py::implicitly_convertible<Var, LinExpr>();
  /*
    m.def("__le__", [](const double x, const double y) -> TempConstr {
          return LinExpr(x) <= LinExpr(y);
    }, py::is_operator());
    m.def("__ge__", [](const double x, const double y) -> TempConstr {
          return LinExpr(x) >= LinExpr(y);
    }, py::is_operator());
    m.def("__eq__", [](const double x, const double y) -> TempConstr {
          return LinExpr(x) >= LinExpr(y);
    }, py::is_operator());
  */

  py::enum_<ErrorCode>(m, "ErrorCode")
      .value("ERROR_SUCCESS", ErrorCode::ERROR_SUCCESS)
      .value("ERROR_BOUND_WRONG", ErrorCode::ERROR_BOUND_WRONG)
      .value("ERROR_NAME_CONFLICT", ErrorCode::ERROR_NAME_CONFLICT)
      .value("ERROR_BOOL_BOUND_WRONG", ErrorCode::ERROR_BOOL_BOUND_WRONG)
      .value("ERROR_NO_SUCH_NAME", ErrorCode::ERROR_NO_SUCH_NAME)
      .value("ERROR_NO_SUCH_TYPE", ErrorCode::ERROR_NO_SUCH_TYPE)
      .value("ERROR_NO_SUCH_VAR", ErrorCode::ERROR_NO_SUCH_VAR)
      .value("ERROR_QUANT_NOT_EQUAL", ErrorCode::ERROR_QUANT_NOT_EQUAL)
      .value("ERROR_INVALID_SENSE", ErrorCode::ERROR_INVALID_SENSE)
      .value("ERROR_REDUND_OPRT", ErrorCode::ERROR_REDUND_OPRT)
      .value("ERROR_OBJ_UNSET", ErrorCode::ERROR_OBJ_UNSET)
      .value("ERROR_LINEAR_EXPR_NO_SUCH_NAME",
             ErrorCode::ERROR_LINEAR_EXPR_NO_SUCH_NAME)
      .value("ERROR_MODEL_DEL_NO_SUCH_NAME",
             ErrorCode::ERROR_MODEL_DEL_NO_SUCH_NAME)
      .value("ERROR_SET_VAL_OUT_BOUND", ErrorCode::ERROR_SET_VAL_OUT_BOUND)
      .value("ERROR_LINEAR_QUANT_NOT_EQUL",
             ErrorCode::ERROR_LINEAR_QUANT_NOT_EQUL)
      .value("ERROR_READ_MPS_ERR", ErrorCode::ERROR_READ_MPS_ERR)
      .value("ERROR_INTERUPTED", ErrorCode::ERROR_INTERUPTED)
      .value("ERROR_VAR_NOT_IN_MODEL", ErrorCode::ERROR_VAR_NOT_IN_MODEL)
      .value("ERROR_NO_SOLUTION_YET", ErrorCode::ERROR_NO_SOLUTION_YET)
      .value("ERROR_VAR_ALREADY_FIXED", ErrorCode::ERROR_VAR_ALREADY_FIXED)
      .export_values();

  py::class_<EventHandler, PyEventHandler, std::shared_ptr<EventHandler>>(m, "EventHandler")
    .def(py::init<>())
    .def("handle", &EventHandler::handle);

  m.attr("errorMessages") = py::cast(errorMessages);

  /*
  py::class_<Exception>(m, "PyException")   // Use a different class name to
  prevent clashes .def(py::init<ErrorCode>(), py::arg("errcode") =
  ErrorCode::ERROR_SUCCESS) .def(py::init<ErrorCode, std::string>(),
  py::arg("errcode"), py::arg("message")) .def("getMessage",
  &Exception::getMessage) .def("getErrorCode", &Exception::getErrorCode)
    .def("__str__", [](const Exception &exc) {
        return exc.what();
    });
  */

  py::register_exception<Exception>(
      m, "Exception"); // Now register the exception for use in Python

  py::class_<Model>(m, "Model")
      .def(py::init<Env &>(), py::arg("env"))
      .def(py::init<Env &, const std::string &>(), py::arg("env"),
           py::arg("name"))
      .def("setInitalVal", &Model::setInitalVal)
      .def("printStats", &Model::printStats)
      .def("getMpsStr", &Model::getMpsStr)
      .def("getJSONSolution", &Model::getJSONSolution)
      .def("getStatus", &Model::getStatus)
      .def("setStatus", &Model::setStatus)
      .def("getSolStatus", &Model::getSolStatus)
      .def("setSolStatus", &Model::setSolStatus)
      .def("attachEventHandler", &Model::attachEventHandler)
      .def("detachEventHandler", &Model::detachEventHandler)
      .def("notifyEventHandlers", &Model::notifyEventHandlers)
      .def("reset", &Model::reset, py::arg("clearall") = 0)
      .def("close", &Model::close)
      .def("getName", &Model::getName)
      .def("setName", &Model::setName)
      .def("getSolText", &Model::getSolText)
      .def("readMPS", &Model::readMPS)
      .def("writeMPS", &Model::writeMPS)
      .def("getVarByName", &Model::getVarByName)
      .def("getConstrByName", &Model::getConstrByName)
      .def("getObj", &Model::getObj)
      .def("getObjVal", &Model::getObjVal)
      .def("remove", py::overload_cast<const Constr &>(&Model::remove))
      .def("remove", py::overload_cast<const Var &>(&Model::remove))
      .def("optimize", &Model::optimize)
      .def("optimize_async", &Model::optimize_async)
      .def("wait", &Model::wait)
      .def("terminate", &Model::terminate)
      .def("printSol", &Model::printSol)
      .def("getVars", &Model::getVars)
      .def("getConstrs", &Model::getConstrs)
      .def("addVar", py::overload_cast<const std::string &>(&Model::addVar))
      .def("addVar", py::overload_cast<const VType &, const std::string &>(
                         &Model::addVar))
      .def("addVar",
           py::overload_cast<const double, const double, const VType &,
                             const std::string &>(&Model::addVar))
      .def("addVars", py::overload_cast<const int>(&Model::addVars))
      .def("addVars",
           py::overload_cast<
               const std::vector<double> &, const std::vector<double> &,
               const std::vector<VType> &, const std::vector<std::string> &>(
               &Model::addVars))
      .def("setObj", &Model::setObj)
      .def("addConstrs",
           py::overload_cast<
               const std::vector<LinExpr> &, const std::vector<std::string> &,
               const std::vector<double> &, const std::vector<std::string> &>(
               &Model::addConstrs))
      .def("addConstrs", py::overload_cast<const std::vector<TempConstr> &,
                                           const std::vector<std::string> &>(
                             &Model::addConstrs))
.def("addConstr", 
    py::overload_cast<const LinExpr &, const std::string &, const LinExpr &, const std::string &>(&Model::addConstr),
    py::arg("lhs"), py::arg("sense"), py::arg("rhs"), py::arg("name")="")
.def("addConstr",
    py::overload_cast<const LinExpr &, const std::string &, const double, const std::string &>(&Model::addConstr),
    py::arg("lhs"), py::arg("sense"), py::arg("rhs"), py::arg("name")="")
.def("addConstr",
    py::overload_cast<const TempConstr &, const std::string &>(&Model::addConstr),
    py::arg("tmp"), py::arg("name")="");
}
