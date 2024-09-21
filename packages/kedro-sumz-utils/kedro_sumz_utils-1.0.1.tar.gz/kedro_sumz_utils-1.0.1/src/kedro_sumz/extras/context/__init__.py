"""Custom Kedro-Virgo context class."""
import logging
from pathlib import Path
from typing import Any, Dict, Union

from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from pluggy import PluginManager

logger = logging.getLogger(__name__)


class KedroSparkContext(KedroContext):
    """Custom kedro context which initializes the Spark Session."""

    def __init__(
        self,
        package_name: str,
        project_path: Union[str, Path],
        config_loader: ConfigLoader,
        hook_manager: PluginManager,
        env: str = None,
        extra_params: Dict[str, Any] = None,
    ):
        logger.info("Creating Kedro Context")
        super().__init__(
            package_name, project_path, config_loader, hook_manager, env, extra_params
        )
        self._spark_session = None
        self._package_name = (
            package_name if package_name else Path(__file__).parent.name
        )

        if not self._init_databricks():
            self._init_spark()

    def _init_spark(self):
        from pyspark import SparkConf
        from pyspark.sql import SparkSession
        
        if SparkSession.getActiveSession() is None:
            logger.info("Initializing Spark session")
            parameters = self._config_loader["spark"]
            logger.info(parameters)
            spark_conf = SparkConf().setAll(list(parameters.items()))

            spark_session_conf = (
                SparkSession.builder.appName(self._package_name)
                .master("local[*, 4]")
                .config(conf=spark_conf)
            )

            self._spark_session = spark_session_conf.getOrCreate()
            self._spark_session.sparkContext.setLogLevel("WARN")
            logger.info("Spark Web URL: %s", self._spark_session.sparkContext.uiWebUrl)
        else:
            self._spark_session = SparkSession.getActiveSession()

    def _init_databricks(self) -> bool:
        try:
            from databricks.connect import DatabricksSession
            from pyspark.sql import SparkSession

            if SparkSession.getActiveSession() is None:
                logger.info("Initializing Databricks session")
                self._spark_session = DatabricksSession.builder.profile(
                    "connect"
                ).getOrCreate()
            else:
                self._spark_session = SparkSession.getActiveSession()
            return True
        except ImportError:
            logger.info(
                "Databricks Connect is not installed. Initializing Spark session instead."
            )
            return False

    @property
    def spark_session(self):
        """Spark session property."""
        return self._spark_session
