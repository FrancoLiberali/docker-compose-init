package main

import (
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/pkg/errors"
	"github.com/spf13/viper"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
)

// InitConfig Function that uses viper library to parse env variables. If
// some of the variables cannot be parsed, an error is returned
func InitConfig() (*viper.Viper, error) {
	v := viper.New()

	// Configure viper to read env variables with the CLI_ prefix
	v.AutomaticEnv()
	v.SetEnvPrefix("cli")

	// Add env variables supported
	v.BindEnv("id")
	v.BindEnv("server", "address")
	v.BindEnv("loop", "period")
	v.BindEnv("loop", "lapse")

	// Viper uses the precedence order: env and then config.
	v.SetConfigName("config") // name of config file (without extension)
	v.SetConfigType("yaml")
	v.AddConfigPath("/etc/client") // path to look for the config file in
	err := v.ReadInConfig()        // Find and read the config file
	if err != nil {                // Handle errors reading the config file
		log.Infof("Config file not found, using only env vars")
	}

	// Parse time.Duration variables and return an error
	// if those variables cannot be parsed
	if _, err := time.ParseDuration(v.GetString("loop_lapse")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_LAPSE env var as time.Duration.")
	}

	if _, err := time.ParseDuration(v.GetString("loop_period")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_PERIOD env var as time.Duration.")
	}

	v.WriteConfigAs("/etc/client/config-used.yml")

	return v, nil
}

func main() {
	v, err := InitConfig()
	if err != nil {
		log.Fatalf("%s", err)
	}

	clientConfig := common.ClientConfig{
		ServerAddress: v.GetString("server_address"),
		ID:            v.GetString("id"),
		LoopLapse:     v.GetDuration("loop_lapse"),
		LoopPeriod:    v.GetDuration("loop_period"),
	}

	client := common.NewClient(clientConfig)
	client.StartClientLoop()
}
